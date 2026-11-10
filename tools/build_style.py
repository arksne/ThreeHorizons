# -*- coding: utf-8 -*-
"""Ф3.1–3.6, 3.8 · Сборка `GAME_DESIGN/Style.json` из `docs/DESIGN_TOKENS.md`.

HEX не дублируются: парсер читает таблицы `DESIGN_TOKENS.md` — единственный источник палитры.
Отсюда же берутся материалы Roblox, свет и атмосфера, UI-токены, правило приоритета арта (D-001)
и чек-лист gate A-1.

Два выхода:
  GAME_DESIGN/Style.json  — истина для кода (Roblox, валидаторы)
  docs/STYLE_BIBLE.md     — человеческая сводка, генерируется отсюда же

Запуск: python -X utf8 tools/build_style.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS_MD = ROOT / "docs" / "DESIGN_TOKENS.md"
OUT_JSON = ROOT / "GAME_DESIGN" / "Style.json"
OUT_MD = ROOT / "docs" / "STYLE_BIBLE.md"

FACTION_SECTIONS = {
    "Арквейн": "arkvein",
    "Вальмер": "valmer",
    "Гринвальд": "grinwald",
}

# материалы Roblox, которыми разрешено красить (решение: ограничить стоком)
STOCK_MATERIALS = {
    "Slate", "Cobblestone", "WoodPlanks", "Fabric", "Metal",
    "DiamondPlate", "Plaster", "Sandstone", "Limestone", "Marble", "Wood", "Brick",
}


def parse_tables(text: str) -> dict:
    """Возвращает {заголовок секции: [строки таблиц]} — только строки данных, без заголовков."""
    sections: dict[str, list[list[str]]] = {}
    cur = None
    rows: list[list[str]] = []
    for raw in text.split("\n"):
        line = raw.rstrip()
        if line.startswith("## "):
            if cur and rows:
                sections[cur] = rows
            cur = line[3:].strip()
            rows = []
            continue
        if cur and line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            # пропускаем разделитель и шапку таблицы (второй элемент — «---»)
            if all(set(c) <= set("-: ") and c for c in cells):
                continue
            if cells[0] in ("Токен", "Ресурс", "Остров", "Общее", "Параметр"):
                continue
            rows.append(cells)
    if cur and rows:
        sections[cur] = rows
    return sections


def parse_tokens(text: str) -> tuple:
    """Достаёт 21 токен фракций, 7 общих, 3 ресурса, свет и UI."""
    sections = parse_tables(text)

    faction_tokens = {v: [] for v in FACTION_SECTIONS.values()}
    ui_tokens = []
    strategic = []
    lighting_factions = {}
    lighting_common = {}
    fonts = {}

    for head, rows in sections.items():
        name = head.split("—")[0].split("(")[0].strip()

        # --- фракции: | Токен | HEX | Применение | Material |
        if name in FACTION_SECTIONS:
            fid = FACTION_SECTIONS[name]
            for r in rows:
                if len(r) < 4:
                    continue
                tok, hexv, usage, mat = r[0], r[1], r[2], r[3]
                mats = [m.strip() for m in re.split(r"[/,]", mat) if m.strip()]
                faction_tokens[fid].append({
                    "id": tok, "hex": hexv, "usage": usage,
                    "materials": mats,
                    "materialIsStock": all(m in STOCK_MATERIALS for m in mats),
                })
            continue

        # --- общие: | Токен | HEX | Применение |
        if name == "Общие":
            for r in rows:
                if len(r) < 3:
                    continue
                ui_tokens.append({"id": r[0], "hex": r[1], "usage": r[2]})
            continue

        # --- стратегические ресурсы: | Ресурс | HEX | Material | Применение |
        if name.startswith("Стратегические"):
            for r in rows:
                if len(r) < 4:
                    continue
                strategic.append({
                    "id": r[0], "hex": r[1],
                    "material": None if r[2] == "—" else r[2],
                    "usage": r[3],
                })
            continue

        # --- свет по островам: | Остров | ColorTemp | Экспозиция | Насыщенность | Туман | Вода |
        if name == "Свет и атмосфера":
            for r in rows:
                if len(r) < 6:
                    # | Общее | Значение |
                    if len(r) == 2:
                        k, v = r[0], r[1]
                        if k == "Шрифт заголовков UI":
                            fonts["title"] = v
                        elif k == "Шрифт тела UI":
                            fonts["body"] = v
                        elif k == "Радиус скругления":
                            fonts["radiusPx"] = int(re.sub(r"\D", "", v) or 0)
                        elif k == "Рамка":
                            fonts["border"] = v
                        else:
                            lighting_common[_norm_key(k)] = _norm_val(k, v)
                    continue
                fid = FACTION_SECTIONS.get(r[0].split("—")[0].strip())
                if not fid:
                    continue
                lighting_factions[fid] = {
                    "colorTempK": _num(r[1]),
                    "exposure": _num(r[2]),
                    "saturation": _num(r[3]),
                    "fog": r[4] if r[4] != "—" else None,
                    "waterReflectance": _reflectance(r[5]),
                }
            continue

    # шрифты могут быть в «Общем»-подразделе раздела «Свет и атмосфера» — уже собрано выше
    return faction_tokens, ui_tokens, strategic, lighting_factions, lighting_common, fonts


SPECIAL_KEYS = {
    "ветер на дрейф кораблей": "windDriftNote",
}


def _norm_key(k: str) -> str:
    """«Atmosphere Density» → atmosphereDensity, «Шторм Atmosphere Density» → stormAtmosphereDensity."""
    k = k.strip()
    low = k.lower()
    if low in SPECIAL_KEYS:
        return SPECIAL_KEYS[low]
    storm = low.startswith("шторм")
    k = re.sub(r"^Шторм\s+", "", k, flags=re.I)
    camel = re.sub(r"[^A-Za-zА-Яа-я0-9]+(.)", lambda m: m.group(1).upper(), k)
    camel = camel[0].lower() + camel[1:]
    return ("storm" + camel[0].upper() + camel[1:]) if storm else camel


def _reflectance(s: str):
    """«Reflectance 0.4» → 0.4; «—» → None."""
    if s.strip() in ("—", "", "-"):
        return None
    m = re.search(r"(\d+(?:\.\d+)?)", s)
    return float(m.group(1)) if m else None


def _norm_val(k: str, v: str) -> object:
    kl = k.lower()
    if "density" in kl or "haze" in kl or "cover" in kl:
        try:
            return float(v)
        except ValueError:
            return v
    return v


def _num(s: str):
    s = s.strip().replace("−", "-").replace("K", "").replace("+", "")
    if s in ("—", "", "-"):
        return None
    try:
        return float(s) if "." in s else int(s)
    except ValueError:
        return s


def build() -> dict:
    text = TOKENS_MD.read_text(encoding="utf-8")
    ft, ui, strat, lf, lc, fonts = parse_tokens(text)

    n_fac = sum(len(v) for v in ft.values())
    if n_fac != 21:
        raise SystemExit(f"ожидалось 21 токен фракций, разобрано {n_fac} — проверь DESIGN_TOKENS.md")
    if len(ui) != 7:
        raise SystemExit(f"ожидалось 7 общих токенов, разобрано {len(ui)}")
    if len(strat) != 3:
        raise SystemExit(f"ожидалось 3 стратегических ресурса, разобрано {len(strat)}")

    materials = []
    for fid, toks in ft.items():
        for t in toks:
            for m in t["materials"]:
                materials.append({"token": t["id"], "faction": fid, "material": m,
                                  "stock": m in STOCK_MATERIALS})

    return {
        "schemaVersion": 1,
        "status": "APPROVED",
        "generatedFrom": ["docs/DESIGN_TOKENS.md", "docs/VISUAL_DESIGN_BIBLE.md",
                          "docs/THREE_HORIZONS_PROJECT_BIBLE.md#1",
                          "docs/DECISIONS.md#D-001"],
        "note": "Арт-дирекшн: стиль, палитры, материалы, свет, UI-токены, чек-лист gate A-1. "
                "Генерируется из DESIGN_TOKENS.md — парсер tools/build_style.py. "
                "HEX не дублируются: правишь док — меняется здесь.",
        "styleFormula": {
            "formula": "Stylized Realism + Medieval Maritime + Vintage Exploration",
            "axes": [
                {"name": "Stylized Realism", "means": "реалистичные пропорции, упрощённая форма"},
                {"name": "Medieval Maritime", "means": "средневековая морская техника и корабли"},
                {"name": "Vintage Exploration", "means": "винтажная палитра, типографика, ретушь"},
            ],
            "antiExamples": ["фэнтези", "стимпанк", "мультяшно", "гиперреализм"],
        },
        "artPriority": "text",
        "artPriorityNote": "D-001: при конфликте атласа с Master Prompt побеждает текст. "
                           "Атлас — референс формы и палитры, не правил.",
        "knownArtDeviations": [
            {"topic": "фамилия Морвей", "note": "«Моряк» — ошибка, канон «Морвей / Morwey» (C-02)"},
            {"topic": "специализация «фермер»", "note": "это профессия, не боевая специализация (C-03)"},
            {"topic": "«древние руины»", "note": "заброшенные поселения, без мистики (C-08)"},
            {"topic": "площадь Гавани", "note": "0.8×0.6 км, а не 0.48 (C-05)"},
        ],
        "factionTokens": ft,
        "uiTokens": ui,
        "strategicResources": strat,
        "materials": materials,
        "lighting": {"factions": lf, "common": lc},
        "fonts": fonts,
        "gateA1": [
            {"id": "hexFromTokens", "title": "HEX из токенов",
             "check": "все цвета ассета есть в factionTokens/uiTokens/strategicResources"},
            {"id": "scaleSpec", "title": "масштаб по MASTER_SCALE_SPEC",
             "check": "габарит совпадает с заявленным в classes/dimsM"},
            {"id": "nameTH", "title": "имя TH_*",
             "check": "имя начинается с TH_ и в верхнем регистре"},
            {"id": "status", "title": "статус concept|blockout|final|lod",
             "check": "поле status из допустимых"},
            {"id": "materialsMax3", "title": "материалов ≤ 3",
             "check": "len(materials) ≤ 3"},
            {"id": "hasUV", "title": "UV есть",
             "check": "uvLayers > 0"},
            {"id": "lodRatio", "title": "LOD 35 % / 8 %",
             "check": "triL1 ≈ 35 % ±3 % triL0, triL2 ≈ 8 % ±2 % triL0"},
            {"id": "pivotBase", "title": "пивот в основании",
             "check": "origin = base_center, низ модели на y = 0"},
        ],
        "stockMaterials": sorted(STOCK_MATERIALS),
        "counts": {"factionTokens": n_fac, "uiTokens": len(ui),
                   "strategicResources": len(strat), "gateA1": 8},
    }


def write_bible(style: dict) -> None:
    """docs/STYLE_BIBLE.md — человеческая сводка, генерируется отсюда же."""
    L = ["# STYLE BIBLE — арт-дирекшн и стиль", "",
         "> Сгенерировано из `GAME_DESIGN/Style.json` (`tools/build_style.py`).",
         "> Правки — в `docs/DESIGN_TOKENS.md`: он и есть источник HEX.", "",
         "## Стиль", "",
         f"**{style['styleFormula']['formula']}**", ""]
    for a in style["styleFormula"]["axes"]:
        L.append(f"- **{a['name']}** — {a['means']}")
    L += ["", "Не делаем: " + ", ".join(style["styleFormula"]["antiExamples"]), "",
          "## Приоритет", "",
          f"**{style['artPriorityNote']}**", "",
          "Признанные расхождения арта:", ""]
    for d in style["knownArtDeviations"]:
        L.append(f"- {d['topic']} — {d['note']}")
    L += ["", "## Палитры фракций", ""]
    for fid, toks in style["factionTokens"].items():
        L.append(f"### {fid}")
        L.append("")
        L.append("| Токен | HEX | Применение | Материал |")
        L.append("|---|---|---|---|")
        for t in toks:
            L.append(f"| `{t['id']}` | {t['hex']} | {t['usage']} | {', '.join(t['materials'])} |")
        L.append("")
    L += ["## Общие токены UI", "", "| Токен | HEX | Применение |", "|---|---|---|"]
    for t in style["uiTokens"]:
        L.append(f"| `{t['id']}` | {t['hex']} | {t['usage']} |")
    L += ["", "## Стратегические ресурсы", "", "| Ресурс | HEX | Material | Применение |", "|---|---|---|---|"]
    for s in style["strategicResources"]:
        L.append(f"| `{s['id']}` | {s['hex']} | {s['material'] or 'SurfaceAppearance (Ф6)'} | {s['usage']} |")
    L += ["", "## Свет и атмосфера", "", "| Остров | ColorTemp | Экспозиция | Насыщенность | Туман | Вода |",
          "|---|---|---|---|---|---|"]
    for fid, v in style["lighting"]["factions"].items():
        L.append(f"| {fid} | {v['colorTempK']}K | {v['exposure']} | {v['saturation']} | "
                 f"{v['fog'] or '—'} | {v['waterReflectance'] or '—'} |")
    L += ["", "| Общее | Значение |", "|---|---|"]
    for k, v in style["lighting"]["common"].items():
        L.append(f"| {k} | {v} |")
    L += ["", "## Шрифты UI", ""]
    for k, v in style["fonts"].items():
        L.append(f"- **{k}**: {v}")
    L += ["", "## Gate A-1 — чек-лист худконтроля", "",
          "| # | Пункт | Проверка |", "|---|---|---|"]
    for i, g in enumerate(style["gateA1"], 1):
        L.append(f"| {i} | {g['title']} | {g['check']} |")
    L += ["", "Проверка: `python -X utf8 tools/validate_style.py <манифест ассета>` → вердикт по каждому пункту.", ""]
    OUT_MD.write_text("\n".join(L), encoding="utf-8")


def main() -> None:
    style = build()
    OUT_JSON.write_text(json.dumps(style, ensure_ascii=False, indent=1), encoding="utf-8")
    write_bible(style)
    c = style["counts"]
    print(f"OK {OUT_JSON.name}: токенов фракций {c['factionTokens']}, "
          f"UI {c['uiTokens']}, ресурсов {c['strategicResources']}, "
          f"материалов {len(style['materials'])}, gate A-1 {c['gateA1']} пунктов")
    print(f"OK {OUT_MD.name}")


if __name__ == "__main__":
    main()
