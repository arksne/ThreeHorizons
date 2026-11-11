# -*- coding: utf-8 -*-
"""Ф4 · Генерация референсов через Higgsfield CLI (Seedream 5.0 Pro, 2K, free).

Поток: по одному кадру → `higgsfield generate create seedream_v5_pro` → `generate wait` →
скачивание PNG → раскладка по id. Последовательно, как просил пользователь: единый стиль.

Возобновляемый: уже скачанные файлы пропускаются, состояние — в `refs/.state.json`.

Запуск:
    python -X utf8 tools/gen_refs.py --group D            # одна группа (A..I или имя)
    python -X utf8 tools/gen_refs.py --all                # всё, чего нет
    python -X utf8 tools/gen_refs.py --only id1,id2      # точечно
    python -X utf8 tools/gen_refs.py --list              # что есть / чего нет
    python -X utf8 tools/gen_refs.py --status            # состояние очереди
"""
import argparse
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
CLOUD = REFS / "cloud"
STATE = REFS / ".state.json"
REG = ROOT / "docs" / "roadmap" / "model-classes.json"

MODEL = "seedream_v5_pro"          # Seedream 5.0 Pro
RESOLUTION = "2k"                  # по умолчанию у модели
ASPECT = "1:1"

# Стиль — единая формула для всей серии
STYLE = ("Stylized Realism + Medieval Maritime + Vintage Exploration. "
         "Realistic proportions, simplified forms. Desaturated vintage palette, "
         "soft even studio lighting, NO dramatic shadows, NO rim light. "
         "Faint film grain, slight sepia at the edges.")
NO_TEXT = ("No text, no letters, no numbers, no labels, no watermark, "
           "no signatures, no UI overlay.")
SCALE_NOTE = ("Include a scale bar with regular tick marks and a 1.7 m human "
              "silhouette next to the object for scale reference.")
GRAY = "flat neutral grey background #B8BEB4"

PAL = {
    "arkvein": ("grey stone #5A5C60, dark timber #4A3226, graphite slate roof #2B2E33, "
                "burgundy accent #6E2A2A, copper #8C5A3B, steel #9AA2A8, plaster #C9C2B4"),
    "valmer": ("limestone #EDE6D3, cream #D9C9A8, sandstone #B99B6B, teal #4E7E8C, "
               "deep sea blue #2E4E7E, bronze #A87F3F, white stone #F5F1E6"),
    "grinwald": ("olive #5A6B3C, forest green #3E5230, warm wood #6B4A2E, beige #D8C9A3, "
                 "straw #C2A35C, terracotta #A55A35, grey stone #8A8578"),
}
NEUTRAL = "dark timber #4A3226, copper #8C5A3B"
UI_PAL = ("parchment #E8DCC0, secondary #CBB98F, brass #B08D3E, ink #1E1A14, "
          "dark wood #3A2A1C, danger #8C2B1B, accent #2E4E7E")
CLOUD_PAL = ("cloud light #EDE6D3, cloud silver #C9C2B4, cloud shadow #A9A396, "
             "distant haze #CBB98F, pale sky #B8BEB4")


# ------------------------------------------------------------------ higgsfield CLI
def _cli_path() -> str:
    """Путь к higgsfield: npm ставит .cmd/.ps1, а Python их не выполняет."""
    import shutil
    from pathlib import Path as _P
    cand = _P(os.environ["APPDATA"]) / "npm" / "higgsfield.cmd"
    if cand.exists():
        return str(cand)
    found = shutil.which("higgsfield")
    if found:
        return found
    raise SystemExit("higgsfield CLI не найден (npm i -g @higgsfield/cli)")


def hf(*args, timeout=180):
    r = subprocess.run([_cli_path(), *args], capture_output=True, text=True,
                       encoding="utf-8", timeout=timeout, cwd=str(ROOT))
    return (r.stdout or "") + (r.stderr or "")


def hf_json(*args, timeout=180):
    out = hf(*args, "--json", timeout=timeout)
    m = re.search(r"\{.*\}", out, re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return {}


def create_job(prompt: str, aspect: str = ASPECT) -> str | None:
    """Создаёт job и возвращает его id."""
    out = hf("generate", "create", MODEL, "--prompt", prompt,
             "--aspect-ratio", aspect, "--resolution", RESOLUTION, timeout=300)
    m = re.search(r"\b([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\b", out)
    return m.group(1) if m else None


def wait_job(job_id: str, timeout_s=600) -> str | None:
    """Ждёт завершения, возвращает URL."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        out = hf("generate", "wait", job_id, timeout=180)
        u = re.search(r"(https?://\S+?\.png)", out)
        if u:
            return u.group(1)
        if re.search(r"\b(failed|error)\b", out, re.I):
            return None
        time.sleep(4)
    return None


def download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=180) as r:
            dest.write_bytes(r.read())
        return dest.stat().st_size > 10000
    except Exception as e:
        print(f"    !! скачивание не удалось: {e}")
        return False


# ------------------------------------------------------------------ промпты
def prompt_for(c: dict) -> str:
    cid, name, grp = c["id"], c["name"], c["group"]
    size = c["sizeM"]
    size_txt = "" if size in ("—", None) else f"Real size {size} m. "

    base = f"{size_txt}Technical reference sheet for a game asset. {STYLE} "
    head = f"Subject: {name}. "

    # --- персонажи ---
    if grp == "char_bodies":
        return (f"{base}A neutral adult human body for a game character, shown full body, "
                f"standing in a plain neutral undergarment — simple light linen briefs/shirt, "
                f"no clothing, no accessories, no footwear. Ordinary human proportions, "
                f"neutral calm face, no exaggerated features. {GRAY}, {SCALE_NOTE}. {NO_TEXT}")

    if grp == "char_npcs":
        return (f"{base}A full-body NPC character: {name.replace('NPC: ', '')}. "
                f"Sheet of THREE views in one row: FRONT, SIDE, BACK. Neutral standing pose, "
                f"arms slightly away from the body so the clothing reads, no weapon in the hands. "
                f"Ordinary human face, calm expression, no monstrous or evil-looking features. "
                f"Height 1.7 m. {GRAY}, even soft lighting. {SCALE_NOTE}. {NO_TEXT}")

    if grp == "characters":
        spec = {
            "char_hero_m": "Adrian Vale, 24-year-old male engineer, reddish-brown skin, dark work coat, leather tool belt, practical boots, sleeves rolled up",
            "char_hero_f": "Eliana Vale, 24-year-old female engineer, the same face and clothes as the male version",
            "char_npc_civil": "an ordinary middle-aged townsperson in plain everyday clothes, nothing remarkable",
            "char_npc_sailor": "a sailor: coarse tunic, belt, rolled sleeves, worn boots",
            "char_npc_pirate": "a pirate in battered dark clothes, an eyepatch, an earring. ORDINARY CALM FACE — no monstrous features",
        }.get(cid, name)
        return (f"{base}A full-body character: {spec}. Sheet of THREE views in one row: FRONT, "
                f"SIDE, BACK. Neutral standing pose, no weapon. {GRAY}, even soft lighting. "
                f"Height 1.7 m. {SCALE_NOTE}. {NO_TEXT}")

    # --- одежда ---
    if grp == "clothing":
        return (f"{base}A single medieval garment laid flat and photographed as a product "
                f"shot: {name}. Show the whole piece clearly, front view, no person wearing "
                f"it. Medieval maritime working-class clothing, hand-made, worn but intact. "
                f"{GRAY}, even soft lighting. {SCALE_NOTE}. {NO_TEXT}")

    # --- корабли ---
    if grp == "ships":
        if "mast" in cid:
            return (f"{base}A single ship mast with yards and rigging, one tall mast with a "
                    f"sail on the yard, side and three-quarter views. {SCALE_NOTE}. {NO_TEXT}")
        if "rudder" in cid:
            return (f"{base}A single ship rudder, close-up, weathered wood and iron pintles, "
                    f"side and three-quarter views. {SCALE_NOTE}. {NO_TEXT}")
        return (f"{base}A medieval sailing ship: {name}. Sheet of THREE views in one row: "
                f"three-quarter from slightly above, strict SIDE profile, strict FRONT bow view. "
                f"Accurate proportions, no perspective distortion, no fantasy elements. "
                f"Hull white-stone #F5F1E6 with dark timber #4A3226 and bronze #A87F3F fittings. "
                f"Waterline clearly visible. {SCALE_NOTE}. {NO_TEXT}")

    # --- оружие ---
    if grp == "weapons":
        return (f"{base}A single medieval weapon: {name.replace('Оружие: ', '')}. "
                f"Photographed as a clean product reference sheet on {GRAY}: the whole weapon "
                f"fully visible, side view and three-quarter view, laid or stood upright. "
                f"Hand-forged steel and dark wood, practical working gear, no ornament. "
                f"{SCALE_NOTE}. {NO_TEXT}")

    # --- детали построек ---
    if grp == "details":
        return (f"{base}A single modular building detail: {name.replace('Деталь: ', '')}. "
                f"Shown as a clean isolated part on {GRAY}, slightly angled so the form reads, "
                f"whole piece visible, no context. Hand-made medieval maritime construction, "
                f"weathered wood and stone. {SCALE_NOTE}. {NO_TEXT}")

    # --- предметы/ресурсы ---
    if grp == "items":
        return (f"{base}A single tradeable item: {name.replace('Предмет: ', '')}. "
                f"Shown as a clean product reference on {GRAY}, whole object visible, "
                f"three-quarter view. Medieval working goods. {SCALE_NOTE}. {NO_TEXT}")

    # --- инструменты ---
    if grp == "tools":
        return (f"{base}A set of medieval trade tools: {name}. Laid out neatly in a row on "
                f"{GRAY}, every tool visible, top-down three-quarter view. "
                f"Worn working tools, hand-forged steel and wood. {SCALE_NOTE}. {NO_TEXT}")

    # --- погода ---
    if grp == "weather":
        return (f"{base}A single weather element: {name}. Shown as a FLAT 2D sprite, large, "
                f"centered on {GRAY}, soft dissolving edges, no volume, no hard boundary, "
                f"no cotton-wool puffiness. Even flat lighting. {NO_TEXT}")

    # --- UI ---
    if grp == "ui":
        return (f"{base}FLAT UI element, drawn strictly front-on, NO perspective, NO tilt: "
                f"{name.replace('UI: ', '')}. Palette exactly: {UI_PAL}. Plain mid-grey page "
                f"background so the element shape reads. Empty plates and lines instead of "
                f"letters. {NO_TEXT}")

    # --- тайлы ---
    if grp == "tiles":
        return (f"{base}A seamless TILE of {name.replace('тайл)', '').strip()}. "
                f"Show it as a 2x2 grid of identical squares so the tiling seam is visible — "
                f"the seam must NOT show, the four squares must flow into each other. "
                f"Viewed straight from above, NO perspective. Even flat lighting. {NO_TEXT}")

    # --- частицы ---
    if grp == "particles":
        return (f"{base}A single flat 2D sprite of {name.lower()}, shown LARGE and centered on "
                f"{GRAY}. It must read as a FLAT image with soft transparent edges, not a 3D "
                f"object, no volume, no cast shadow. {NO_TEXT}")

    # --- облака ---
    if grp == "clouds":
        if cid == "cloud_puff":
            return (f"{base}One single flat translucent cloud wisp as a 2D sprite, front view, "
                    f"centered on {GRAY}, soft dissolving brush-stroke edges, no volume, no hard "
                    f"boundary, no volumetric look. {CLOUD_PAL}. {NO_TEXT}")
        return (f"{base}A single flat TILE of the {name.lower()} cloud layer, shown as a 2x2 "
                f"grid of identical squares so the tiling seam is visible, viewed straight from "
                f"above with no perspective. The tile must be seamless: no visible edge between "
                f"the four squares. {CLOUD_PAL}. {NO_TEXT}")

    # --- здания ---
    if grp == "buildings":
        spec = {
            "bld_house_small": "8x10 m, 1-2 storeys, plain and unadorned, one door, 2-3 small windows",
            "bld_house_medium": "10x14 m, 2-3 storeys, plain, possible ridge beam, two windows per floor",
            "bld_house_large": "14x18 m, wider and taller, facade with plaster ornament and shutters of another colour, possible balcony",
            "bld_shop": "12x18 m, ground floor with a wide shopfront opening, awning, plain sign board",
            "bld_tavern": "18x24 m, tall windows, second floor, hanging sign, barrels by the wall",
            "bld_workshop": "12x20 m, anvil by the entrance, forge, open lean-to shed, tools by the wall",
            "bld_warehouse": "20x35 m, big panelled cargo doors, roof dormers, almost no windows, flat roof",
            "bld_dock": "40x14 m timber pier on stilts, bollards, a lantern, railings, meeting the water",
            "bld_tower": "8x8 m, 3 storeys, top storey corbelled out, stone base, clock on the front face",
            "bld_manor": "20x20 m, corner tower with a conical cap, colonnaded porch, entrance steps, balcony",
            "bld_wall": "10x3x2 m section of town wall with crenellations and a walkway - a repeating fragment, not a house",
            "bld_gate": "6x4 m city gate with an arch, double doors, a small tower on each side - a repeating fragment",
        }.get(cid, name)
        return (f"{base}A medieval harbour building: {spec}. Sheet of THREE views in one row: "
                f"three-quarter from slightly above, strict FRONT elevation, strict SIDE elevation. "
                f"Accurate proportions, no perspective distortion, no fantasy elements. "
                f"Materials: {PAL['arkvein']}. Clear material boundaries, no colour blending. "
                f"Even flat lighting, no dramatic shadows. {SCALE_NOTE}. {NO_TEXT}")

    # --- мир/рельеф ---
    if grp == "world":
        spec = {
            "terr_island": ("a floating rock island 1200x900 m seen whole from a distance: expressive "
                            "rugged rock base, uneven slopes, surface terrain, terraces, clear flat "
                            "building sites. NO flat bottom - the base dissolves into cloud. "
                            "One island only, no neighbours"),
            "terr_rock": "three different grey boulders 2x2x3 m with cracks, side by side",
            "terr_tree": "three different broadleaf trees 6x4 m with irregular crowns, side by side",
            "terr_grass": "three different low bushes and grass tufts 0.5 m, side by side",
            "terr_farm": "a 20x10 m farm plot: vegetable beds, a fence, tilled earth, some hay",
            "terr_windmill": "a stone windmill 8x12 m with wooden sails and a canvas sail",
            "terr_aqueduct": "a 20 m stone aqueduct with arches and a water channel on top",
            "terr_bridge": "a 12x4 m timber bridge with railings on stone piers",
        }.get(cid, name)
        pal = PAL["grinwald"] if cid not in ("terr_island",) else PAL["arkvein"]
        return (f"{base}{spec}. {GRAY}, even soft lighting, no dramatic shadows. "
                f"Materials: {pal}. {SCALE_NOTE}. {NO_TEXT}")

    # --- пропы ---
    if grp == "props":
        spec = {
            "prop_barrel": "a wooden barrel 0.6x0.9 m with metal hoops and a lid",
            "prop_crate": "a wooden crate 0.8x0.8 m with planks and metal corner brackets",
            "prop_bench": "a wooden bench 1.8x0.5 m with a backrest and iron legs",
            "prop_table": "a plain rough-hewn wooden table 1.2x0.75 m, completely empty",
            "prop_stall": "a market stall 2x1 m with a canopy and shelves, completely empty",
            "prop_anchor": "a ship anchor 1.2 m with rope, traces of rust",
            "prop_lamp": "a lantern 0.4x1.2 m on a bracket, brass, warm light inside",
            "prop_crane": "a timber dock crane 4x3x6 m, a rope with a hook",
        }.get(cid, name)
        return (f"{base}A single game prop: {spec}. Centered on {GRAY}, even soft lighting. "
                f"Materials: {NEUTRAL}. {SCALE_NOTE}. {NO_TEXT}")

    # --- окружение ---
    if grp == "environment":
        spec = {
            "env_sea": "a seamless TILE of a cloud sea surface: smooth milky water, cool #2E4E7E tint, soft highlights",
            "env_waves": "a seamless TILE of soft waves with light foam",
            "env_terrain": "a seamless 100x100 m TILE of terrain: stone, soil and grass with smooth transitions",
            "env_road": "a seamless STRIP of cobbled road with a kerb along both edges, 100x4 m",
            "env_rail": "a seamless STRIP of railway rails on sleepers with ballast, 100x2 m",
        }.get(cid, name)
        return (f"{base}{spec}. Show it as a 2x2 grid of identical squares so the tiling seam is "
                f"visible - the seam must NOT show. Viewed straight from above, NO perspective. "
                f"Even flat lighting. {NO_TEXT}")

    return f"{base}{name}. {GRAY}, even lighting. {SCALE_NOTE}. {NO_TEXT}"


# ------------------------------------------------------------------ очередь
def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"done": {}, "failed": {}, "jobs": {}}


def save_state(st: dict) -> None:
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def load_classes() -> list:
    return json.loads(REG.read_text(encoding="utf-8"))["classes"]


def dest_for(c: dict) -> Path:
    if c["group"] in ("clouds", "weather"):
        return CLOUD / f"{c['id']}.png"
    if c["group"] == "buildings":
        return REFS / f"{c['id']}.png"
    return REFS / f"{c['id']}.png"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--group")
    ap.add_argument("--only")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    classes = load_classes()
    state = load_state()

    if args.status:
        done = len(state.get("done", {}))
        failed = len(state.get("failed", {}))
        print(f"готово {done} | ошибок {failed} | всего в реестре {len(classes)}")
        for k, v in list(state.get("failed", {}).items())[:10]:
            print(f"  !! {k}: {v}")
        return

    if args.list:
        for c in classes:
            d = dest_for(c)
            mark = "OK " if d.exists() else "— "
            print(f"  {mark}{c['id']:34} {c['group']:14} {c['sizeM']}")
        return

    sel = classes
    LETTERS = ["particles", "clouds", "ships", "buildings", "world", "characters",
               "props", "ui", "environment", "char_bodies", "char_npcs", "clothing",
               "weapons", "details", "items", "tools", "weather", "tiles"]
    if args.group:
        g = args.group.strip().lower()
        if len(g) == 1 and g.upper() in "ABCDEFGHI":
            g = LETTERS[ord(g.upper()) - ord("A")]
        sel = [c for c in classes if c["group"].lower() == g]
        if not sel:
            raise SystemExit(f"группа не найдена. Доступные: {', '.join(LETTERS)}")
    if args.only:
        only = {x.strip() for x in args.only.split(",")}
        sel = [c for c in classes if c["id"] in only]

    todo = [c for c in sel if not dest_for(c).exists()]
    if args.limit:
        todo = todo[: args.limit]
    print(f"к генерации: {len(todo)} (в группе {len(sel)}, уже есть {len(sel) - len(todo)})")
    if not todo:
        print("нечего делать")
        return

    for n, c in enumerate(todo, 1):
        cid = c["id"]
        prompt = prompt_for(c)
        print(f"\n[{n}/{len(todo)}] {cid} — {c['name'][:44]}")
        job = create_job(prompt)
        if not job:
            print("  !! job не создан")
            state.setdefault("failed", {})[cid] = "job не создан"
            save_state(state)
            continue
        state.setdefault("jobs", {})[cid] = job
        save_state(state)
        print(f"  job {job}")
        url = wait_job(job)
        if not url:
            print("  !! не дождался")
            state.setdefault("failed", {})[cid] = "timeout/failed"
            save_state(state)
            continue
        dest = dest_for(c)
        if download(url, dest):
            state.setdefault("done", {})[cid] = {"job": job, "file": str(dest.relative_to(ROOT))}
            state.get("failed", {}).pop(cid, None)
            save_state(state)
            print(f"  OK {dest.relative_to(ROOT)} ({dest.stat().st_size // 1024} KB)")
        else:
            state.setdefault("failed", {})[cid] = "download failed"
            save_state(state)

    print(f"\nготово {len(state.get('done', {}))} | ошибок {len(state.get('failed', {}))}")


if __name__ == "__main__":
    main()
