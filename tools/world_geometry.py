# -*- coding: utf-8 -*-
"""Единая геометрия мира Three Horizons (Ф2).

Один источник истины для координат, размеров, высот и таймингов.
Рамка — решение S-07: атлас + карта 18×26 км игровых. Позиции островов —
по композиции атласа, размеры — из `WORLD_MASTER_MAP.md` (C-01, C-07),
высоты — относительные доли (S-08), столицы — по MASTER_MAP (S-09).

Всё считается из `GAME_DESIGN/constants.json`: ни одна цифра не дублируется.

Запуск: python -X utf8 tools/world_geometry.py [--dump]
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONST = json.loads((ROOT / "GAME_DESIGN" / "constants.json").read_text(encoding="utf-8"))

SCALE = CONST["scale"]
WORLD = CONST["world"]
HEIGHTS = WORLD["heights"]

M_TO_STUDS = SCALE["metersToStuds"]          # 3.571 (S-01)
COMPRESS = SCALE["worldCompression"]          # 0.1  (S-02)
MAP_W_M = WORLD["mapKm"][0] * 1000            # 18 000 м игровых
MAP_D_M = WORLD["mapKm"][1] * 1000            # 26 000 м игровых
SEA_Y = WORLD["seaY"]

# Острова: центр в лор-км (как в атласе) → игровые м → studs.
# loreX/loreZ — центр острова в лор-км; размеры — лор-км (C-01: 12×9 и т.д.).
ISLANDS = [
    {
        "id": "arkvein", "name": "Арквейн", "faction": "arkvein",
        "loreX": 90, "loreZ": 40, "loreW": 12, "loreD": 9,
        "heightM": 280, "capital": "arkenhold", "capitalSizeM": [250, 200],
        "role": "Производство: корабли, механизмы, инженерия",
    },
    {
        "id": "valmer", "name": "Вальмер", "faction": "valmer",
        "loreX": 150, "loreZ": 115, "loreW": 24, "loreD": 18,
        "heightM": 210, "capital": "valmara", "capitalSizeM": [300, 250],
        "role": "Вода: добыча/очистка/хранение/распределение",
    },
    {
        "id": "grinwald", "name": "Гринвальд", "faction": "grinwald",
        "loreX": 72, "loreZ": 210, "loreW": 25, "loreD": 19,
        "heightM": 165, "capital": "grinholm", "capitalSizeM": [300, 250],
        "role": "Продукты питания",
    },
    {
        "id": "esterholm", "name": "Эстерхольм", "faction": None,
        "loreX": 108, "loreZ": 130, "loreW": 1.5, "loreD": 1,
        "heightM": 190, "capital": None, "capitalSizeM": [150, 100],
        "role": "Нейтральный порт: исследования, точка встречи трёх сюжетов",
    },
    {
        "id": "black_harbor", "name": "Чёрная Гавань", "faction": None,
        "loreX": 30, "loreZ": 115, "loreW": 0.8, "loreD": 0.6,
        "heightM": 170, "capital": None, "capitalSizeM": [80, 60],
        "role": "Пиратский свободный порт и торговый узел, чёрный рынок (C-11)",
    },
]

# Мини-острова (S-10): в Ф2 только 4 промысловых, остальные 6 мест — резерв на Ф9.
# Позиции в лор-км, внутри карты 0..180 × 0..260; ≥ 600 st (168 м) до ближайшего острова.
MINI_ISLANDS = [
    {"id": "A1", "name": "Рыболовный форпост", "loreX": 30, "loreZ": 20,
     "loreW": 0.42, "loreD": 0.3, "role": "Промысловый: рыба"},
    {"id": "A2", "name": "Соляной промысел", "loreX": 160, "loreZ": 30,
     "loreW": 0.42, "loreD": 0.3, "role": "Промысловый: соль"},
    {"id": "A3", "name": "Лесозаготовка", "loreX": 150, "loreZ": 230,
     "loreW": 0.42, "loreD": 0.3, "role": "Промысловый: лес"},
    {"id": "A4", "name": "Рудник", "loreX": 20, "loreZ": 230,
     "loreW": 0.42, "loreD": 0.3, "role": "Промысловый: руда"},
]

# Маршруты грузоперевозок (C-11: Pirate Base отдельным островом не вводим).
# pirate_raid идёт по тому же плечу, что arkvein_hub, но тип contraband — на карте рисуется пунктиром.
ROUTES = [
    {"id": "arkvein_hub", "from": "arkvein", "to": "black_harbor", "type": "cargo"},
    {"id": "valmer_hub", "from": "valmer", "to": "black_harbor", "type": "cargo"},
    {"id": "grinwald_hub", "from": "grinwald", "to": "black_harbor", "type": "cargo"},
    {"id": "esterholm_hub", "from": "esterholm", "to": "black_harbor", "type": "cargo"},
    {"id": "pirate_raid", "from": "black_harbor", "to": "arkvein", "type": "contraband"},
]

SPEED_M_S = 18.0   # скорость среднего корпуса (Bible §4)


def m_to_studs(m: float) -> float:
    return m * M_TO_STUDS


def lore_to_game_m(km: float) -> float:
    """Лор-км → игровые м (сжатие 1:10, S-02)."""
    return km * 1000.0 * COMPRESS


def heights_for(height_m: float) -> dict:
    """S-08: низ/плато/пик — доли игровой высоты; Y=0 = облачное море."""
    low = round(height_m * HEIGHTS["low"], 1)
    plateau = round(height_m * HEIGHTS["plateau"], 1)
    peak = round(height_m * HEIGHTS["peak"], 1)
    return {
        "seaY": SEA_Y,
        "lowM": low, "lowY": round(m_to_studs(low)),
        "plateauM": plateau, "plateauY": round(m_to_studs(plateau)),
        "peakM": peak, "peakY": round(m_to_studs(peak)),
    }


def build_island(raw: dict) -> dict:
    game_x = lore_to_game_m(raw["loreX"])
    game_z = lore_to_game_m(raw["loreZ"])
    game_w = lore_to_game_m(raw["loreW"])
    game_d = lore_to_game_m(raw["loreD"])
    return {
        "id": raw["id"],
        "name": raw["name"],
        "faction": raw["faction"],
        "role": raw["role"],
        "loreXM": raw["loreX"] * 1000,
        "loreZM": raw["loreZ"] * 1000,
        "loreWM": raw["loreW"] * 1000,
        "loreDM": raw["loreD"] * 1000,
        "gameXM": round(game_x, 1),
        "gameZM": round(game_z, 1),
        "gameWM": round(game_w, 1),
        "gameDM": round(game_d, 1),
        "studsX": round(m_to_studs(game_x)),
        "studsZ": round(m_to_studs(game_z)),
        "studsW": round(m_to_studs(game_w)),
        "studsD": round(m_to_studs(game_d)),
        "heightM": raw["heightM"],
        "heights": heights_for(raw["heightM"]),
        "capital": raw["capital"],
        "capitalSizeM": raw["capitalSizeM"],
    }


def build_mini(raw: dict) -> dict:
    game_x = lore_to_game_m(raw["loreX"])
    game_z = lore_to_game_m(raw["loreZ"])
    game_w = lore_to_game_m(raw["loreW"])
    game_d = lore_to_game_m(raw["loreD"])
    return {
        "id": raw["id"],
        "name": raw["name"],
        "role": raw["role"],
        "loreXM": raw["loreX"] * 1000,
        "loreZM": raw["loreZ"] * 1000,
        "loreWM": raw["loreW"] * 1000,
        "loreDM": raw["loreD"] * 1000,
        "gameXM": round(game_x, 1),
        "gameZM": round(game_z, 1),
        "gameWM": round(game_w, 1),
        "gameDM": round(game_d, 1),
        "studsX": round(m_to_studs(game_x)),
        "studsZ": round(m_to_studs(game_z)),
        "studsW": round(m_to_studs(game_w)),
        "studsD": round(m_to_studs(game_d)),
    }


def islands() -> list[dict]:
    return [build_island(i) for i in ISLANDS]


def mini_islands() -> list[dict]:
    return [build_mini(m) for m in MINI_ISLANDS]


def bounds(isl: dict) -> tuple:
    return (isl["gameXM"] - isl["gameWM"] / 2, isl["gameXM"] + isl["gameWM"] / 2,
            isl["gameZM"] - isl["gameDM"] / 2, isl["gameZM"] + isl["gameDM"] / 2)


def distance_m(a: dict, b: dict) -> float:
    dx = a["gameXM"] - b["gameXM"]
    dz = a["gameZM"] - b["gameZM"]
    return (dx * dx + dz * dz) ** 0.5


def travel_times() -> dict:
    """Времена перелётов: скорость среднего корпуса, сжатие уже учтено в координатах."""
    by_id = {i["id"]: i for i in islands()}
    out = {}
    for r in ROUTES:
        a, b = by_id[r["from"]], by_id[r["to"]]
        d = distance_m(a, b)
        secs = d / SPEED_M_S
        out[r["id"]] = {
            "from": r["from"],
            "to": r["to"],
            "type": r["type"],
            "distanceGameM": round(d, 1),
            "distanceStuds": round(m_to_studs(d)),
            "distanceLoreKm": round(d / (1000 * COMPRESS), 2),
            "seconds": round(secs),
            "minutes": round(secs / 60, 1),
            "speedMs": SPEED_M_S,
        }
    return out


def world() -> dict:
    return {
        "frame": "S-07 (атлас + карта 18×26 км игровых)",
        "metersToStuds": M_TO_STUDS,
        "worldCompression": COMPRESS,
        "mapGameM": [MAP_W_M, MAP_D_M],
        "mapStuds": WORLD["mapStuds"],
        "seaY": SEA_Y,
        "islands": islands(),
        "miniIslands": mini_islands(),
        "travelTimes": travel_times(),
    }


if __name__ == "__main__":
    import sys
    w = world()
    if "--dump" in sys.argv:
        print(json.dumps(w, ensure_ascii=False, indent=1))
    else:
        print(f"OK рамка {w['frame']}")
        print(f"   карта {w['mapGameM'][0]:.0f}×{w['mapGameM'][1]:.0f} м "
              f"= {w['mapStuds'][0]}×{w['mapStuds'][1]} st")
        for i in w["islands"]:
            h = i["heights"]
            print(f"   {i['name']:12} игр.м ({i['gameXM']:7.0f},{i['gameZM']:7.0f}) "
                  f"size {i['gameWM']:6.0f}×{i['gameDM']:6.0f} | "
                  f"Y низ {h['lowY']:5} плато {h['plateauY']:5} пик {h['peakY']:5}")
        for m in w["miniIslands"]:
            print(f"   {m['id']} {m['name']:20} ({m['gameXM']:7.0f},{m['gameZM']:7.0f}) {m['role']}")
        for rid, t in w["travelTimes"].items():
            print(f"   {rid:16} {t['distanceGameM']:8.0f} м = {t['minutes']:4.1f} мин")
