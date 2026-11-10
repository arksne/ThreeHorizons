# -*- coding: utf-8 -*-
"""
Генератор роадмап-канвасов для Obsidian (читаемая раскладка).

Выход:
  ROADMAP_0.1.canvas           — индекс: 12 фаз крупными карточками + решения + грабли
  docs/roadmap/canvas/phase-XX.canvas — отдельный канвас на фазу: шаги крупно + сайдбар
                                        (Definition of Done / риски / чего не делаем)

Запуск: python -X utf8 tools/make_roadmap_canvas.py
"""
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHASES_DIR = ROOT / "docs" / "roadmap"
OUT_DIR = PHASES_DIR / "canvas"
INDEX_OUT = ROOT / "ROADMAP_0.1.canvas"

RED, ORANGE, YELLOW, GREEN, CYAN, PURPLE = "1", "2", "3", "4", "5", "6"
CRITICAL = {0, 1, 2, 6, 8, 9, 10, 11}
PROGRESS_FILE = ROOT / "docs" / "PROGRESS.json"
STATUS_COLOR = {"done": GREEN, "in_progress": YELLOW, "blocked": RED,
                "skipped": ORANGE, "todo": CYAN}
STATUS_MARK = {"done": "✅ ", "in_progress": "🟨 ", "blocked": "🟥 ", "skipped": "⏭ "}


def load_progress() -> dict:
    if not PROGRESS_FILE.exists():
        return {}
    try:
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8")).get("steps", {})
    except Exception:
        return {}

CARD_GAP = 22
STEP_W = 620
SIDE_W = 420
SIDE_GAP = 40


# ---------------------------------------------------------------- парсинг

def parse_phase(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = next((l[2:].strip() for l in lines if l.startswith("# ")), "?")
    goal = next((l.split("**Цель:**", 1)[1].strip() for l in lines if "**Цель:**" in l), "")

    sections = {"dod": [], "risks": [], "notdo": []}
    section = None
    steps, cur, field = [], None, None

    for line in lines:
        if line.startswith("## "):
            head = line[3:].strip().lower()
            section = ("dod" if head.startswith("definition of done")
                       else "risks" if head.startswith("риски")
                       else "notdo" if head.startswith("чего в этой фазе")
                       else None)
            cur, field = None, None
            continue
        m = re.match(r"###\s+(\S+)\s*·\s*(.+)", line)
        if m:
            cur = {"num": m.group(1), "title": m.group(2).strip(),
                   "action": "", "tool": "", "done": "", "canon": ""}
            steps.append(cur)
            field, section = None, None
            continue
        if section and line.strip().startswith("-"):
            item = re.sub(r"^-\s*(\[ \]\s*)?", "", line).strip()
            if item:
                sections[section].append(item)
            continue
        if cur is None:
            continue
        m = re.match(r"-\s+\*\*(Действие|Инструмент|Результат|Готово, когда|Канон):\*\*\s*(.*)", line)
        if m:
            field = {"Действие": "action", "Инструмент": "tool",
                     "Готово, когда": "done", "Канон": "canon"}.get(m.group(1))
            if field:
                cur[field] = m.group(2).strip()
            continue
        if re.match(r"-\s+\*\*", line):
            field = None
            continue
        if field and line.strip():
            cur[field] = (cur[field] + " " + line.strip()).strip()
    return {"title": title, "goal": goal, "steps": steps, **sections}


# ---------------------------------------------------------------- геометрия

def wrap_lines(text: str, chars: int) -> int:
    """Перенос по словам: точнее, чем деление длины на ширину."""
    total = 0
    for para in text.split("\n"):
        para = para.replace("**", "").replace("`", "").strip()
        if not para:
            total += 1
            continue
        line_len, lines = 0, 1
        for word in para.split(" "):
            w = len(word)
            if line_len == 0:
                line_len = w
                if w > chars:  # длинный токен ломается на несколько строк
                    lines += math.ceil(w / chars) - 1
                    line_len = w % chars or chars
            elif line_len + 1 + w <= chars:
                line_len += 1 + w
            else:
                lines += 1
                line_len = w
        total += lines
    return total


def measure(text: str, width: int) -> int:
    chars = max(18, int(width / 9.2))
    head = 0
    body_lines = 0
    for para in text.split("\n"):
        if para.startswith("### "):
            head += max(1, math.ceil(len(para) / chars))
        else:
            body_lines += wrap_lines(para, chars)
    return 28 + head * 28 + body_lines * 24 + 26


def node(nid, text, x, y, w, color=None, h=None):
    return {
        "id": nid, "type": "text", "text": text,
        "x": x, "y": y, "width": w,
        "height": h if h else measure(text, w),
        **({"color": color} if color else {}),
    }


def group(gid, label, x, y, w, h):
    return {"id": gid, "type": "group", "label": label,
            "x": x, "y": y, "width": w, "height": h}


def edge(eid, a, b, color=CYAN, fs="right", ts="left"):
    return {"id": eid, "fromNode": a, "fromSide": fs,
            "toNode": b, "toSide": ts, "color": color}


# ---------------------------------------------------------------- канвас фазы

def build_phase_canvas(idx: int, ph: dict, md_name: str, progress: dict) -> dict:
    nodes, edges = [], []
    steps = ph["steps"]
    done = sum(1 for s in steps if progress.get(s["num"]) == "done")

    # заголовок
    crit = " · ⭐ критический путь" if idx in CRITICAL else ""
    head = (f"# {ph['title']}{crit}\n"
            f"**Цель:** {ph['goal']}\n\n"
            f"**{len(steps)} шагов · готово {done}/{len(steps)}** · файл: [[{md_name}]] · "
            f"индекс: [[ROADMAP_0.1]]")
    nodes.append(node(f"p{idx}_head", head, 0, -190, STEP_W + SIDE_W + SIDE_GAP, PURPLE))

    # шаги — крупные карточки
    y = 0
    for s in steps:
        status = progress.get(s["num"], "todo")
        mark = STATUS_MARK.get(status, "")
        text = f"### {mark}{s['num']} · {s['title']}\n{s['action']}"
        if s.get("tool"):
            text += f"\n🛠 {s['tool']}"
        if s.get("done"):
            text += f"\n**✔ Готово, когда:** {s['done']}"
        if s.get("canon"):
            text += f"\n_Канон: {s['canon']}_"
        nodes.append(node(f"p{idx}_s{s['num'].replace('.', '_')}", text, 0, y, STEP_W,
                          STATUS_COLOR.get(status, CYAN)))
        y += measure(text, STEP_W) + CARD_GAP

    # сайдбар
    sx = STEP_W + SIDE_GAP
    side_y = 0
    blocks = [
        ("Definition of Done", ph["dod"], GREEN, "☐ "),
        ("Риски и грабли", ph["risks"], ORANGE, "• "),
        ("Чего в этой фазе НЕ делаем", ph["notdo"], RED, "— "),
    ]
    for name, items, color, bullet in blocks:
        if not items:
            continue
        text = f"**{name}**\n" + "\n".join(bullet + i for i in items)
        nodes.append(node(f"p{idx}_{name[:4]}", text, sx, side_y, SIDE_W, color))
        side_y += measure(text, SIDE_W) + CARD_GAP

    edges.append(edge(f"p{idx}_e", f"p{idx}_head", f"p{idx}_s{steps[0]['num'].replace('.', '_')}", PURPLE))
    return {"nodes": nodes, "edges": edges}


# ---------------------------------------------------------------- индекс

def build_index(phases: list[dict], md_names: list[str], progress: dict) -> dict:
    nodes, edges = [], []
    total = sum(len(p["steps"]) for p in phases)
    done_total = sum(1 for p in phases for s in p["steps"] if progress.get(s["num"]) == "done")
    title = (
        "# THREE HORIZONS — ROADMAP 0.1\n"
        f"**12 фаз · {total} шагов · готово {done_total}** · база создана 2026-11-10 · [[ROADMAP_0.1]]\n"
        "Клик по ссылке в карточке фазы → отдельный канвас с крупными шагами.\n"
        "Статусы берутся из `docs/PROGRESS.json`; критический путь: Ф0 → Ф1 → Ф2 → Ф6 → Ф8 → Ф9 → Ф10 → Ф11."
    )
    nodes.append(node("idx_title", title, 0, -260, 980, PURPLE))

    legend = (
        "**Как пользоваться**\n"
        "• 🟦 не начато · 🟨 в работе · 🟩 готово · 🟥 риск — цвет карточки-шага.\n"
        "• В карточке фазы: `phase-XX` — канвас шагов, `phase-XX-...` — полный текст.\n"
        "• Шаг закрыт, только когда выполнен критерий «✔ Готово, когда».\n"
        "• Статус шага: `python -X utf8 tools/make_progress.py 0.1 done` → пересобрать канвас."
    )
    nodes.append(node("idx_legend", legend, 1010, -260, 520, CYAN))

    # сетка фаз 3×N, высота строки — по самой высокой карточке
    texts, colors = [], []
    for i, ph in enumerate(phases):
        mark = " ⭐" if i in CRITICAL else ""
        done = sum(1 for s in ph["steps"] if progress.get(s["num"]) == "done")
        texts.append(
            f"# {ph['title']}{mark}\n"
            f"**Цель:** {ph['goal']}\n\n"
            f"**{len(ph['steps'])} шагов · готово {done}** · "
            f"[[phase-{i:02d}.canvas|открыть шаги]] · [[{md_names[i]}|полный текст]]"
        )
        colors.append(GREEN if done == len(ph["steps"]) else YELLOW if done else CYAN)

    cols, cw, ch_gap = 3, 660, 50
    heights = [measure(t, cw) for t in texts]
    rows = math.ceil(len(phases) / cols)
    pos, y = {}, 0
    for r in range(rows):
        row_h = max(heights[r * cols:(r + 1) * cols]) + 46
        for c in range(cols):
            i = r * cols + c
            if i >= len(phases):
                break
            nodes.append(node(f"ph{i}", texts[i], c * (cw + ch_gap), y, cw,
                              colors[i], h=heights[i]))
            pos[i] = (r, c)
        y += row_h
    grid_bottom = y

    for i in range(len(phases) - 1):
        same_row = pos[i][0] == pos[i + 1][0]
        edges.append(edge(f"ie{i}", f"ph{i}", f"ph{i + 1}", CYAN,
                          "right" if same_row else "bottom",
                          "left" if same_row else "top"))

    base_y = grid_bottom + 110

    decisions = [
        ("S-01 · Метр в studs", "3 или 3.571 в доках. Рекомендация: 3.571 (1 st = 0.28 м).", YELLOW),
        ("S-02 · Сжатие мира", "1:10 vs 1:20. Рекомендация: 1:10 по горизонтали и вертикали.", YELLOW),
        ("S-03 · Размер карты", "18×26 км игровых; 168 км² — лор-текст.", YELLOW),
        ("S-04 · Шард", "60 игроков на старте, поднять после профилирования.", YELLOW),
        ("S-05 · Вода", "Terrain-вода только near-зоной 2–4 км + туман на горизонте.", YELLOW),
        ("S-06 · Облака", "Меш-облака запрещены. Слои: Clouds + клочья + Atmosphere.", YELLOW),
    ]
    for i, (t, b, c) in enumerate(decisions):
        nodes.append(node(f"d{i}", f"**{t}**\n{b}", (i % 3) * 500, base_y + 80 + (i // 3) * 190, 470, c))
    nodes.append(group("dec_group", "РЕШЕНИЯ ДО СТАРТА · Ф0.11 → [[DECISIONS]]",
                       0, base_y, 1480, 520))

    grabli = (
        "**Грабли — читать перед каждым шагом**\n"
        "• Меш-облака = «вата»: нет просвечивания и мягкого края.\n"
        "• `AlignPosition` OneAttachment держит XZ → корабль не разгоняется.\n"
        "• `Enum.OrientationAlignmentMode`, а не выдуманный тип.\n"
        "• `Enum.Font.Serif` не существует → Garamond / Merriweather.\n"
        "• `StarterPlayerScripts` нельзя репарентать.\n"
        "• `Clouds` только под `Workspace.Terrain`.\n"
        "• FBX в Studio — только руками (3D Importer).\n"
        "• EditableMesh на клиенте ≈ 8 мешей.\n"
        "• `Terrain.Size` read-only, но FillBall/FillBlock пишут и дальше.\n"
        "• Blender — `--threads 2`, BelowNormal.\n"
        "• Пивот — в основании по центру; MeshPart ≤ 9 500 tri."
    )
    nodes.append(node("grabli", grabli, 1540, base_y + 80, 620, RED))
    nodes.append(group("grabli_group", "ГРАБЛИ", 1520, base_y, 660, 640))
    return {"nodes": nodes, "edges": edges}


def main() -> None:
    files = sorted(PHASES_DIR.glob("phase-*.md"))
    if not files:
        raise SystemExit("нет docs/roadmap/phase-*.md")

    phases, md_names = [], []
    progress = load_progress()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for idx, path in enumerate(files):
        ph = parse_phase(path)
        phases.append(ph)
        md_names.append(path.stem)
        canvas = build_phase_canvas(idx, ph, path.stem, progress)
        out = OUT_DIR / f"phase-{idx:02d}.canvas"
        out.write_text(json.dumps(canvas, ensure_ascii=False, indent=1), encoding="utf-8")

    index = build_index(phases, md_names, progress)
    INDEX_OUT.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(len(p["steps"]) for p in phases)
    print(f"OK index {INDEX_OUT.name} | phases={len(files)} | steps={total}")
    print(f"OK phase canvases -> {OUT_DIR}")


if __name__ == "__main__":
    main()
