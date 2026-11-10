# -*- coding: utf-8 -*-
"""Ф2.8 · Сетка кварталов столицы Аркенхольд (250×200 м).

Раскладка: сетка 4×2 с восемью районами по `world/CITY_LAYOUTS.md` (решение C-10 —
по игровой структуре). Улицы: главная 8 м, второстепенные 4 м (MASTER_SCALE_SPEC §3).
Каждый квартал получает прямоугольник, список зданий из `Buildings.json` и признак
`waterfront` (у воды — торговая гавань с причалом).

Запуск: python -X utf8 tools/build_arkenhold.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GD = ROOT / "GAME_DESIGN"

CITY_W, CITY_D = 250, 200     # игровые м (S-09)
STREET_MAIN, STREET_SEC = 8, 4
GAP = 3                        # пожарный разрыв между домами (MASTER_SCALE_SPEC §3)
DOCK = [40, 14]

# Районы Арквейна по CITY_LAYOUTS (C-10). Порядок = чтение сетки 4×2, сверху вниз.
DISTRICTS = [
    # id,           название,               колонка, ряд, waterfront, набор зданий
    ("central_square", "Центральная площадь", 0, 0, False, ["tavern", "house_medium", "house_medium"]),
    ("residential",    "Жилой квартал",        1, 0, False, ["house_small", "house_small", "house_medium"]),
    ("industrial",     "Промышленная зона",    2, 0, False, ["workshop", "warehouse", "house_small"]),
    ("shipyard",       "Большая верфь",       3, 0, False, ["workshop", "warehouse", "house_medium"]),
    ("engineering",    "Инженерный квартал",   0, 1, False, ["workshop", "house_medium", "house_small"]),
    ("metallurgy",     "Металлургический район", 1, 1, False, ["workshop", "warehouse", "house_medium"]),
    ("warehouses",     "Склады",               2, 1, False, ["warehouse", "house_large", "house_small"]),
    ("trade_harbor",   "Торговая гавань",      3, 1, True,  ["shop", "house_medium", "house_small"]),
]


def block_rects() -> list:
    """Прямоугольники 8 кварталов: 4 колонки × 2 ряда, между — улицы.

    Вертикальные улицы: главная 8 м (между колонками 0|1 и 2|3), второстепенная 4 м (между 1|2).
    Горизонтальная: главная 8 м между рядами.
    Ширина: 4 полосы кварталов по 57.5 м + 20 м улиц = 250 м.
    Высота: 2 полосы кварталов по 96 м + 8 м улица = 200 м.
    """
    total_v = STREET_MAIN + STREET_SEC + STREET_MAIN      # 20 м улиц по вертикали
    col_w = (CITY_W - total_v) / 4                        # 57.5 м на колонку
    row_h = (CITY_D - STREET_MAIN) / 2                     # 96 м на ряд

    # начало каждой колонки: предыдущая + её ширина + улица после неё
    col_x = [0.0]
    for i in range(4):
        street_after = STREET_MAIN if i in (0, 2) else STREET_SEC
        col_x.append(col_x[-1] + col_w + street_after)
    row_z = [0.0, row_h + STREET_MAIN]                    # ряд 1 начинается за главной улицей

    out = []
    for did, name, col, row, water, kinds in DISTRICTS:
        out.append(dict(id=did, name=name,
                        x=round(col_x[col], 2), z=round(row_z[row], 2),
                        w=round(col_w, 2), d=round(row_h, 2),
                        waterfront=water, buildingKinds=kinds))
    return out


def street_rects() -> list:
    """Прямоугольники улиц — чтобы сумма кварталов + улиц = площадь города."""
    total_v = STREET_MAIN + STREET_SEC + STREET_MAIN
    col_w = (CITY_W - total_v) / 4
    row_h = (CITY_D - STREET_MAIN) / 2

    out = []
    col_x = [0.0]
    for i in range(4):
        street_after = STREET_MAIN if i in (0, 2) else STREET_SEC
        col_x.append(col_x[-1] + col_w + street_after)
    # вертикальные улицы: между колонками
    for i in range(3):
        w = STREET_MAIN if i in (0, 2) else STREET_SEC
        out.append(dict(id=f"street_v{i}", kind="main" if w == STREET_MAIN else "secondary",
                        x=round(col_x[i] + col_w, 2), z=0.0, w=round(w, 2), d=round(CITY_D, 2),
                        orientation="vertical"))
    # горизонтальная главная — между рядами
    out.append(dict(id="street_h0", kind="main",
                    x=0.0, z=round(row_h, 2), w=round(CITY_W, 2), d=round(STREET_MAIN, 2),
                    orientation="horizontal"))
    return out


def place_buildings(block: dict, classes: dict, street_side: str) -> list:
    """Раскладывает здания ВДОЛЬ улицы: фасад к ней, в ряд, с зазором GAP.

    street_side: "south" — улица внизу квартала (фасад смотрит в +Z),
                 "north" — улица сверху (фасад смотрит в −Z).
    Размеры здания: w вдоль улицы, d вглубь квартала.
    """
    w, d = block["w"], block["d"]
    placed = []
    x = 0.0
    for kind in block["buildingKinds"]:
        bw, bd = classes[kind]["sizeM"]
        if bw > w - GAP * 2 or bd > d - GAP * 2:
            continue
        if x + bw > w:
            break                      # в ряд не влезает — следующий ряд будет в Ф9
        if street_side == "south":
            bz = d - bd               # фасад у нижней (уличной) грани
        else:
            bz = 0.0
        placed.append({"kind": kind, "x": round(x, 2), "z": round(bz, 2),
                       "w": bw, "d": bd, "rotationDeg": 0,
                       "facade": street_side})
        x += bw + GAP
    return placed


def main() -> None:
    b = json.loads((GD / "Buildings.json").read_text(encoding="utf-8"))
    classes = {c["id"]: c for c in b["classes"]}

    blocks = block_rects()
    streets = street_rects()
    # каждый квартал знает, с какой стороны улица: ряд 0 — снизу (юг), ряд 1 — сверху (север)
    for blk in blocks:
        side = "south" if blk["z"] < CITY_D / 2 else "north"
        blk["streetSide"] = side
        blk["buildings"] = place_buildings(blk, classes, side)

    # причал: у торговой гавани, с водной стороны (восточный край города)
    harbor = next(b_ for b_ in blocks if b_["waterfront"])
    harbor["dock"] = {"kind": "dock", "x": round(harbor["w"] + GAP, 2),
                      "z": round(harbor["d"] / 2 - DOCK[1] / 2, 2),
                      "w": DOCK[0], "d": DOCK[1], "rotationDeg": 0}

    area = sum(b_["w"] * b_["d"] for b_ in blocks)
    sarea = sum(s["w"] * s["d"] for s in streets)
    total = CITY_W * CITY_D

    data = {
        "schemaVersion": 1,
        "status": "APPROVED",
        "generatedFrom": ["docs/world/CITY_LAYOUTS.md", "GAME_DESIGN/Buildings.json",
                          "docs/MASTER_SCALE_SPEC.md#3", "docs/DECISIONS.md#S-09",
                          "docs/DECISIONS.md#C-10"],
        "note": "Сетка кварталов Аркенхольда. Районы — по CITY_LAYOUTS (C-10). "
                "Здания стоят вдоль улицы фасадом к ней, с зазором 3 м (пожарный разрыв). "
                "Раскладка зданий — базовая, Ф9 уточнит по контексту.",
        "city": "arkenhold",
        "citySizeM": [CITY_W, CITY_D],
        "grid": {"cols": 4, "rows": 2,
                 "streetMainM": STREET_MAIN, "streetSecondaryM": STREET_SEC,
                 "buildingGapM": GAP,
                 "note": "Вертикальные улицы: главная 8 м (между 0|1 и 2|3), "
                         "второстепенная 4 м (между 1|2). Горизонтальная: главная 8 м между рядами."},
        "waterSide": "east",
        "blocks": blocks,
        "streets": streets,
        "totals": {"blockAreaM2": round(area, 1), "streetAreaM2": round(sarea, 1),
                   "cityAreaM2": total, "blockShare": round(area / total, 4),
                   "note": "Кварталы + улицы = площадь города (проверяется validate_world)."},
    }
    p = GD / "arkenhold_blocks.json"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"OK {p.name}: кварталов {len(blocks)}, улиц {len(streets)}, зданий "
          f"{sum(len(b_['buildings']) for b_ in blocks)} + 1 причал")
    print(f"   кварталы {area:.0f} м² ({area / total * 100:.1f} %) + "
          f"улицы {sarea:.0f} м² ({sarea / total * 100:.1f} %) = {area + sarea:.0f} / {total}")
    for b_ in blocks:
        print(f"   {b_['id']:16} {b_['x']:6.1f},{b_['z']:5.1f} "
              f"{b_['w']:5.1f}×{b_['d']:5.1f}  "
              f"{len(b_['buildings'])} зд.  {'у воды' if b_['waterfront'] else ''}")


if __name__ == "__main__":
    main()
