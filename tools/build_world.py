# -*- coding: utf-8 -*-
"""Ф2.2–2.4 · Генерация данных геометрии мира.

Из `GAME_DESIGN/constants.json` (через `tools/world_geometry.py`) собирает:
  - `GAME_DESIGN/World.json`      — источник истины по геометрии
  - `docs/world/WORLD_COORDINATES.csv` — человекочитаемый экспорт (с комментариями)
  - `GAME_DESIGN/travel_times.json`   — времена перелётов

Руками не править ни один из них: пересчёт идёт из constants.json.

Запуск: python -X utf8 tools/build_world.py
"""
import csv
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import world_geometry as wg  # noqa: E402

GD = ROOT / "GAME_DESIGN"
WORLD_DOCS = ROOT / "docs" / "world"

CSV_HEADER = ["id", "kind", "name", "role", "loreX", "loreZ", "loreW", "loreD",
              "gameX", "gameZ", "gameW", "gameD",
              "studsX", "studsZ", "studsW", "studsD",
              "surfaceY", "plateauY", "peakY", "heightM"]

CSV_COMMENT = [
    "# Карта мира Three Horizons — координаты островов и мини-островов.",
    "# Рамка S-07: атлас + карта 18×26 км игровых (18000×26000 м = 64278×92846 st).",
    "# 1 лор-км = 100 игровых м (сжатие 1:10, S-02); st = м × 3.571 (S-01).",
    "# Y: 0 = облачное море; низ/плато/пик — доли игровой высоты острова (S-08).",
    "# kind: island = полный остров, mini = мини-остров (42×30 м игровых).",
    "# У мини-островов высот нет (surfaceY/plateauY/peakY пустые) — они плоские.",
    "# Источник истины: GAME_DESIGN/World.json (генерируется tools/build_world.py).",
    "# В расчёты не идёт: docs/world/ISLAND_CATALOG.md и WORLD_SCALE.md — старая рамка.",
]


def build_world() -> dict:
    islands = wg.islands()
    mini = wg.mini_islands()
    travel = wg.travel_times()
    const = wg.CONST
    return {
        "schemaVersion": 1,
        "status": "APPROVED",
        "generatedFrom": [
            "docs/WORLD_MASTER_MAP.md",
            "docs/MASTER_SCALE_SPEC.md",
            "docs/world/ISLAND_CATALOG.md",
            "docs/DECISIONS.md#S-07",
            "docs/DECISIONS.md#S-08",
            "docs/DECISIONS.md#S-10",
        ],
        "note": "Геометрия мира. Рамка S-07 (атлас + 18×26 км игровых). "
                "Генерируется из constants.json — руками не править.",
        "frame": {
            "id": "S-07",
            "mapGameM": [const["world"]["mapKm"][0] * 1000, const["world"]["mapKm"][1] * 1000],
            "mapStuds": const["world"]["mapStuds"],
            "metersToStuds": const["scale"]["metersToStuds"],
            "worldCompression": const["scale"]["worldCompression"],
            "seaY": const["world"]["seaY"],
            "heights": const["world"]["heights"],
        },
        "islands": islands,
        "miniIslands": mini,
        "travelTimes": travel,
    }


def write_world_json(world: dict) -> Path:
    p = GD / "World.json"
    p.write_text(json.dumps(world, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


def write_csv(world: dict) -> Path:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")

    def row(i: dict, mini: bool = False) -> list:
        if mini:
            return [i["id"], "mini", i["name"], i["role"],
                    i["loreXM"] / 1000, i["loreZM"] / 1000, i["loreWM"] / 1000, i["loreDM"] / 1000,
                    i["gameXM"], i["gameZM"], i["gameWM"], i["gameDM"],
                    i["studsX"], i["studsZ"], i["studsW"], i["studsD"],
                    "", "", "", ""]
        h = i["heights"]
        return [i["id"], "island", i["name"], i["role"],
                i["loreXM"] / 1000, i["loreZM"] / 1000, i["loreWM"] / 1000, i["loreDM"] / 1000,
                i["gameXM"], i["gameZM"], i["gameWM"], i["gameDM"],
                i["studsX"], i["studsZ"], i["studsW"], i["studsD"],
                h["lowY"], h["plateauY"], h["peakY"], i["heightM"]]

    w.writerow(CSV_HEADER)
    for i in world["islands"]:
        w.writerow(row(i))
    for m in world["miniIslands"]:
        w.writerow(row(m, mini=True))

    p = WORLD_DOCS / "WORLD_COORDINATES.csv"
    p.write_text("\n".join(CSV_COMMENT) + "\n" + buf.getvalue(), encoding="utf-8")
    return p


def write_travel_times(world: dict) -> Path:
    data = {
        "schemaVersion": 1,
        "status": "APPROVED",
        "generatedFrom": ["GAME_DESIGN/World.json", "GAME_DESIGN/Routes.json",
                          "docs/THREE_HORIZONS_PROJECT_BIBLE.md#4"],
        "note": "Времена перелётов: скорость среднего корпуса 18 м/с (Bible §4), "
                "координаты игровые — сжатие 1:10 уже учтено. "
                "Проверка: разница с Routes.json ≤ 5 %.",
        "speedMs": 18,
        "routes": list(world["travelTimes"].values()),
    }
    p = GD / "travel_times.json"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


def fill_routes_distances(world: dict) -> Path:
    """Проставляет расстояния в Routes.json из вычисленных (Ф2.7)."""
    p = GD / "Routes.json"
    routes = json.loads(p.read_text(encoding="utf-8"))
    tt = world["travelTimes"]
    for r in routes.get("routes", []):
        t = tt.get(r["id"])
        if not t:
            continue
        r["distanceGameM"] = t["distanceGameM"]
        r["distanceLoreKm"] = t["distanceLoreKm"]
        r["travelSec"] = t["seconds"]
        r["travelMin"] = t["minutes"]
    routes["note"] = ("Маршруты связывают столицы с хабом (Чёрная Гавань). "
                      "Расстояния и время посчитаны в Ф2.7 из GAME_DESIGN/World.json "
                      "(18 м/с, сжатие 1:10 учтено).")
    p.write_text(json.dumps(routes, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


def main() -> None:
    world = build_world()
    p1 = write_world_json(world)
    p2 = write_csv(world)
    p3 = write_travel_times(world)
    p4 = fill_routes_distances(world)

    print(f"OK {p1.name}: островов {len(world['islands'])}, "
          f"мини-островов {len(world['miniIslands'])}, "
          f"маршрутов {len(world['travelTimes'])}")
    print(f"OK {p2.name}: {len(world['islands']) + len(world['miniIslands'])} строк")
    print(f"OK {p3.name}")
    print(f"OK {p4.name}: расстояния проставлены")
    print(f"   карта {world['frame']['mapGameM'][0]:.0f}×{world['frame']['mapGameM'][1]:.0f} м "
          f"= {world['frame']['mapStuds'][0]}×{world['frame']['mapStuds'][1]} st")


if __name__ == "__main__":
    main()
