# -*- coding: utf-8 -*-
"""Ф4 · Генерация референсов через Higgsfield MCP → ART_ASSIGN/REFS.

Поток: батч-генерация (до 12 за раз) → ожидание → скачивание → раскладка по id.
Промпты берутся из `docs/roadmap/model-classes.json` + правил ниже, чтобы
источник истины остался один.

Запуск:
    python -X utf8 tools/gen_refs.py --list
    python -X utf8 tools/gen_refs.py --group D            # одна группа
    python -X utf8 tools/gen_refs.py --all                # всё
    python -X utf8 tools/gen_refs.py --only bld_house_small,ship_medium
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "ART_ASSETS" / "refs"
CLOUD_DIR = REFS / "cloud"
MODEL = "gpt_image_2_6"
HF = ROOT / "tools" / "higgsfield.py"

# ---------------------------------------------------------------- промпты

STYLE = (
    "Stylized Realism + Medieval Maritime + Vintage Exploration: realistic proportions, "
    "simplified forms, desaturated vintage palette, soft even studio lighting, "
    "NO dramatic shadows, no rim light. Vintage film grain, faint sepia at the edges."
)
NO_TEXT = "No text, no letters, no numbers, no watermark, no labels."

FACTION_PALETTE = {
    "arkvein": "grey stone #5A5C60, dark timber #4A3226, graphite slate roof #2B2E33, "
               "burgundy accent #6E2A2A, copper #8C5A3B, steel #9AA2A8, plaster #C9C2B4",
    "valmer": "limestone #EDE6D3, cream #D9C9A8, sandstone #B99B6B, teal #4E7E8C, "
              "deep sea blue #2E4E7E, bronze #A87F3F, white stone #F5F1E6",
    "grinwald": "olive #5A6B3C, forest green #3E5230, warm wood #6B4A2E, beige #D8C9A3, "
                "straw #C2A35C, terracotta #A55A35, grey stone #8A8578",
}
NEUTRAL = "dark timber #4A3226, copper #8C5A3B"

SCALE_NOTE = (
    "Include a scale bar with regular tick marks and a 1.7 m human silhouette next to "
    "the object for scale reference."
)


def prompt_for(c: dict) -> str:
    """Промпт под конкретный класс модели."""
    cid, name, grp = c["id"], c["name"], c["group"]
    size = c["sizeM"]
    size_txt = "" if size == "—" else f"Real size {size} m. "

    base = f"{size_txt}Technical reference sheet for game asset. {STYLE} "
    head = f"Subject: {name}. "

    if grp == "particles":
        return (f"{base}A single flat 2D sprite of {name.lower()}, shown LARGE and centered on a "
                f"flat neutral grey background #B8BEB4. It must read as a FLAT image with soft "
                f"transparent edges, not a 3D object, no volume, no cast shadow. "
                f"Even flat lighting, no rim light. {NO_TEXT}")

    if grp == "clouds":
        if cid == "cloud_puff":
            return (f"{base}One single flat translucent cloud wisp as a 2D sprite, front view, "
                    f"centered on flat neutral grey #B8BEB4, soft dissolving brush-stroke edges, "
                    f"no volume, no hard boundary, no volumetric look, no cotton-wool puffiness. "
                    f"Cloud tones: light #EDE6D3, silver #C9C2B4, shadow #A9A396. {NO_TEXT}")
        return (f"{base}A single flat TILE of the {name.lower()} cloud layer, shown as a "
                f"2x2 grid of identical squares so the tiling seam is visible, viewed straight "
                f"from above with no perspective. The tile must be seamless: no visible edge "
                f"between the four squares. Cloud tones: light #EDE6D3, silver #C9C2B4, "
                f"shadow #A9A396. Flat even lighting, no dramatic shadows. {NO_TEXT}")

    if grp == "ships":
        if cid == "ship_mast":
            return (f"{base}A single ship mast with yards and rigging, one tall mast with a "
                    f"sail on the yard, shown from the side and from three-quarter view, "
                    f"wood #4A3226 and canvas sail. {SCALE_NOTE} {NO_TEXT}")
        if cid == "ship_rudder":
            return (f"{base}A single ship rudder, close-up, weathered wood and iron pintles, "
                    f"shown from the side and from three-quarter view. {SCALE_NOTE} {NO_TEXT}")
        hull = cid.replace("ship_", "")
        spec = {"light": "18x6 m hull, low freeboard, ONE mast up to 14 m, narrow hull, few sails",
                "medium": "32x10 m hull, higher freeboard, TWO masts, deck with cargo hatch",
                "heavy": "48x15 m hull, tall freeboard, THREE masts, thick planking, heavy deck"}[hull]
        return (f"{base}A medieval sailing ship hull: {spec}. Sheet of THREE views in one row: "
                f"three-quarter from slightly above, strict SIDE profile, strict FRONT bow view. "
                f"Accurate proportions, no perspective distortion, no fantasy elements. "
                f"Hull white-stone #F5F1E6 with dark timber #4A3226 and bronze #A87F3F fittings. "
                f"Show the waterline clearly. {SCALE_NOTE} {NO_TEXT}")

    if grp == "buildings":
        spec = {
            "bld_house_small": "8x10 m, 1-2 storeys, plain and unadorned, one door, 2-3 small windows",
            "bld_house_medium": "10x14 m, 2-3 storeys, plain, possible ridge beam, two windows per floor",
            "bld_house_large": "14x18 m, wider and taller, facade with plaster ornament and shutters of another colour, possible balcony",
            "bld_shop": "12x18 m, ground floor with a wide shopfront opening, awning, plain sign board",
            "bld_tavern": "18x24 m, tall windows, second floor, hanging sign, barrels by the wall, the warmest building on the street",
            "bld_workshop": "12x20 m, anvil by the entrance, forge, open lean-to shed, tools and wood shavings by the wall",
            "bld_warehouse": "20x35 m, big panelled cargo doors, roof dormers, almost no windows, flat roof",
            "bld_dock": "40x14 m timber pier on stilts, bollards, a lantern, railings, meeting the water at one side",
            "bld_tower": "8x8 m, 3 storeys, top storey corbelled out, stone base, clock on the front face",
            "bld_manor": "20x20 m, corner tower with a conical cap, colonnaded porch, entrance steps, balcony",
            "bld_wall": "10x3x2 m section of town wall with crenellations and a walkway - a repeating fragment, not a house",
            "bld_gate": "6x4 m city gate with an arch, double doors, a small tower on each side - a repeating fragment, not a house",
        }[cid]
        pal = FACTION_PALETTE["arkvein"]
        return (f"{base}A medieval harbour building: {spec}. Sheet of THREE views in one row: "
                f"three-quarter from slightly above, strict FRONT elevation, strict SIDE elevation. "
                f"Accurate proportions, no perspective distortion, no fantasy elements. "
                f"Materials: {pal}. Clear material boundaries, no colour blending. "
                f"Flat even lighting, no dramatic shadows. {SCALE_NOTE} {NO_TEXT}")

    if grp == "world":
        spec = {
            "terr_island": "a floating rock island 1200x900 m seen whole from a distance: expressive rugged rock base, uneven slopes, surface terrain, terraces, clear flat building sites. NO flat bottom - the base dissolves into cloud. One island only, no neighbours",
            "terr_rock": "three different grey boulders 2x2x3 m with cracks, shown side by side",
            "terr_tree": "three different broadleaf trees 6x4 m with irregular crowns and warm trunks, side by side",
            "terr_grass": "three different low bushes and grass tufts 0.5 m, side by side",
            "terr_farm": "a 20x10 m farm plot: vegetable beds, a fence, tilled earth, some hay",
            "terr_windmill": "a stone windmill 8x12 m with wooden sails and a canvas sail, sails seen from the side",
            "terr_aqueduct": "a 20 m stone aqueduct with arches and a water channel on top - a repeating fragment",
            "terr_bridge": "a 12x4 m timber bridge with railings on stone piers - a repeating fragment",
        }[cid]
        pal = FACTION_PALETTE["grinwald"] if "terr" in cid and cid != "terr_island" else FACTION_PALETTE["arkvein"]
        return (f"{base}{spec}. Plain flat neutral grey background #B8BEB4, even soft lighting, "
                f"no dramatic shadows. Materials: {pal}. {SCALE_NOTE} {NO_TEXT}")

    if grp == "characters":
        spec = {
            "char_hero_m": "Adrian Vale, 24-year-old male engineer of Arkvein, reddish-brown skin, dark work coat, leather tool belt, practical boots, sleeves rolled up",
            "char_hero_f": "Eliana Vale, 24-year-old female engineer of Arkvein, the same face and the same clothes as the male version",
            "char_npc_civil": "an ordinary middle-aged townsperson in plain everyday clothes, nothing remarkable",
            "char_npc_sailor": "a sailor: coarse tunic, belt, rolled sleeves, worn boots",
            "char_npc_pirate": "a pirate in battered dark clothing, an eyepatch, an earring. ORDINARY CALM FACE - no monstrous or evil-looking features, he is distinguished by his clothes and posture only",
        }[cid]
        return (f"{base}A full-body character: {spec}. Sheet of THREE views in one row: FRONT, "
                f"SIDE, BACK. Neutral standing pose, arms slightly away from the body so the "
                f"clothing reads, no weapon in the hands, no action pose. Flat neutral grey "
                f"background #B8BEB4, even soft lighting, no dramatic shadows. Ordinary human "
                f"face, calm expression. Height 1.7 m. {SCALE_NOTE} {NO_TEXT}")

    if grp == "props":
        spec = {
            "prop_barrel": "a wooden barrel 0.6x0.9 m with metal hoops and a lid",
            "prop_crate": "a wooden crate 0.8x0.8 m with planks and metal corner brackets, signs of use",
            "prop_bench": "a wooden bench 1.8x0.5 m with a backrest and iron legs",
            "prop_table": "a plain rough-hewn wooden table 1.2x0.75 m, completely empty, nothing on it",
            "prop_stall": "a market stall 2x1 m with a canopy and shelves, completely empty",
            "prop_anchor": "a ship anchor 1.2 m with rope, traces of rust",
            "prop_lamp": "a lantern 0.4x1.2 m on a bracket, brass, warm light inside",
            "prop_crane": "a timber dock crane 4x3x6 m, a rope with a hook, a working structure",
        }[cid]
        return (f"{base}A single game prop: {spec}. Centered on flat neutral grey background "
                f"#B8BEB4, even soft lighting, no dramatic shadows. Materials: {NEUTRAL}. "
                f"{SCALE_NOTE} {NO_TEXT}")

    if grp == "ui":
        spec = {
            "ui_panel": "a window panel: parchment #E8DCC0, brass frame 2px, thin dividers, dark wood #3A2A1C side panel, corners rounded 4px",
            "ui_button": "a button in THREE states side by side: normal, hover, pressed - brass outline, parchment fill, the difference shows in tone and brightness",
            "ui_scroll": "a scroll list: rows separated by a thin line, a scrollbar on the right with a brass thumb",
            "ui_toast": "a small toast notification: parchment, brass border, soft shadow, one empty text line inside",
            "ui_input": "an empty text input field: brass frame, thin blinking cursor, an overlaid input plate",
        }[cid]
        return (f"{base}FLAT UI element, drawn strictly front-on, NO perspective, NO tilt: {spec}. "
                f"Palette exactly: parchment #E8DCC0, secondary #CBB98F, brass #B08D3E, "
                f"ink #1E1A14, dark wood #3A2A1C, danger #8C2B1B, accent #2E4E7E. "
                f"Plain mid-grey page background so the element shape reads. "
                f"Empty plates and lines instead of letters. {NO_TEXT}")

    if grp == "environment":
        spec = {
            "env_sea": "a seamless TILE of a cloud sea surface: smooth milky water, cool #2E4E7E tint, soft highlights",
            "env_waves": "a seamless TILE of soft waves with light foam",
            "env_terrain": "a seamless 100x100 m TILE of terrain: stone, soil and grass with smooth transitions between them",
            "env_road": "a seamless STRIP of cobbled road with a kerb along both edges, 100x4 m, the strip repeats",
            "env_rail": "a seamless STRIP of railway rails on sleepers with ballast, 100x2 m, the strip repeats",
        }[cid]
        return (f"{base}{spec}. Show it as a 2x2 grid of identical squares so the tiling seam is "
                f"visible - the seam must NOT show, the four squares must flow into each other. "
                f"Viewed straight from above, NO perspective. Even flat lighting. {NO_TEXT}")

    return f"{base}{name}. Plain neutral grey background, even lighting. {NO_TEXT}"


# ---------------------------------------------------------------- higgsfield

def hf_call(tool: str, args: dict) -> str:
    r = subprocess.run([sys.executable, "-X", "utf8", str(HF), "call", tool,
                        json.dumps(args, ensure_ascii=False)],
                       capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    return (r.stdout or "") + (r.stderr or "")


def hf_batch(requests: list) -> list:
    """Батч-генерация. Возвращает список job_id."""
    out = hf_call("generate_image_batch", {"requests": requests})
    ids = re.findall(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", out)
    seen, res = set(), []
    for i in ids:
        if i not in seen:
            seen.add(i); res.append(i)
    return res


URL_RE = re.compile(r'(https://[^\s"]+?\.png)')


def wait_jobs(ids: list, timeout: int = 900) -> dict:
    """Ждёт завершения и возвращает {job_id: url}.

    Ответ jobs_wait — CSV-подобный блок:
        jobs[1]{index,job_id,status,type,model,result_url}:
          0,<job_id>,completed,image,gpt_image_2_6,"https://...png"
    """
    done = {}
    deadline = time.time() + timeout
    while time.time() < deadline and len(done) < len(ids):
        payload = {"jobs": [{"index": i, "job_id": j} for i, j in enumerate(ids)],
                   "timeout_seconds": 15}
        out = hf_call("jobs_wait", payload)
        for line in out.splitlines():
            m = re.match(r"\s*\d+,([0-9a-f-]{36}),(\w+),", line)
            if not m:
                continue
            jid, status = m.group(1), m.group(2)
            if jid in done:
                continue
            if status in ("completed", "succeeded"):
                u = URL_RE.search(line)
                done[jid] = u.group(1) if u else None
            elif status in ("failed", "error", "canceled"):
                done[jid] = None
        if len(done) < len(ids):
            time.sleep(4)
    return done


def download(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "three-horizons-refs"})
        with urllib.request.urlopen(req, timeout=120) as r:
            dest.write_bytes(r.read())
        return True
    except Exception as e:
        print(f"    !! скачивание не удалось: {e}")
        return False


def load_classes() -> list:
    p = ROOT / "docs" / "roadmap" / "model-classes.json"
    return json.loads(p.read_text(encoding="utf-8"))["classes"]


def main() -> None:
    classes = load_classes()
    args = sys.argv[1:]
    if "--list" in args:
        for c in classes:
            print(f"  {c['id']:22} {c['group']:12} {c['sizeM']}")
        return

    sel = classes
    if "--group" in args:
        g = args[args.index("--group") + 1].strip().lower()
        # допускаем и букву группы (A..I), и её имя (particles)
        LETTERS = ["particles", "clouds", "ships", "buildings", "world",
                   "characters", "props", "ui", "environment"]
        if len(g) == 1 and g.upper() in "ABCDEFGHI":
            g = LETTERS[ord(g.upper()) - ord("A")]
        sel = [c for c in classes if c["group"].lower() == g]
        if not sel:
            raise SystemExit(f"группа не найдена. Доступные: {', '.join(LETTERS)} (или A..I)")
    if "--only" in args:
        only = set(args[args.index("--only") + 1].split(","))
        sel = [c for c in classes if c["id"] in only]
    if "--all" in args:
        sel = classes

    REFS.mkdir(parents=True, exist_ok=True)
    todo = [c for c in sel if not (REFS / f"{c['id']}.png").exists()]
    print(f"к генерации: {len(todo)} (уже есть: {len(sel) - len(todo)})")
    if not todo:
        print("нечего делать")
        return

    # по одному: сгенерировали → дождались → скачали → следующий
    # (батчи дают плохую раскладку по стилю при большом объёме)
    for c in todo:
        req = {"index": 0,
               "params": {"model": MODEL, "prompt": prompt_for(c), "aspect_ratio": "1:1"}}
        print(f"\n[{c['id']}] {c['name']} ({c['sizeM']}) — отправка…")
        ids = hf_batch([req])
        if not ids:
            print("  !! job не создан")
            continue
        jid = ids[0]
        urls = wait_jobs([jid], timeout=420)
        url = urls.get(jid)
        if not url:
            print("  !! не готово / упало")
            continue
        dest = REFS / f"{c['id']}.png"
        if download(url, dest):
            print(f"  OK {dest.relative_to(ROOT)} ({dest.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
