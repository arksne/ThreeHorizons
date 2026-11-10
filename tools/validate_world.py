# -*- coding: utf-8 -*-
"""Ф2.6 · Валидатор геометрии мира.

Проверяет:
  1. все объекты внутри границ карты 18×26 км
  2. острова (и мини-острова) не пересекаются
  3. маршруты не проходят сквозь острова
  4. расстояния ≥ минимума (мини-островы — ≥ 600 st от островов; острова — ≥ 2 км друг от друга)
  5. координаты CSV == GAME_DESIGN/World.json
  6. сумма кварталов столицы ≈ площади города (±10 %), причал у воды
  7. ступени высот: плато − низ ≥ 20 % игровой высоты

Запуск: python -X utf8 tools/validate_world.py
Итог:   WORLD OK  (exit 0)  или  WORLD FAIL + список расхождений (exit 1)
"""
import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GD = ROOT / "GAME_DESIGN"
WORLD_DOCS = ROOT / "docs" / "world"

MINI_ISLAND_MIN_STUDS = 600      # Ф2.3
ISLAND_MIN_DIST_M = 2000         # между островами
BLOCK_AREA_TOLERANCE = 0.10      # ±10 % (Ф2.8)
DOCK_SIZE_M = [40, 14]           # MASTER_SCALE_SPEC §3

errors: list[str] = []
notes: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def ok(msg: str) -> None:
    notes.append(msg)


def load_world() -> dict:
    return json.loads((GD / "World.json").read_text(encoding="utf-8"))


def rect(i: dict) -> tuple:
    return (i["gameXM"] - i["gameWM"] / 2, i["gameXM"] + i["gameWM"] / 2,
            i["gameZM"] - i["gameDM"] / 2, i["gameZM"] + i["gameDM"] / 2)


def overlap(a: dict, b: dict) -> bool:
    ax0, ax1, az0, az1 = rect(a)
    bx0, bx1, bz0, bz1 = rect(b)
    return (ax0 < bx1 and bx0 < ax1) and (az0 < bz1 and bz0 < az1)


def seg_hits_rect(p0: tuple, p1: tuple, r: tuple) -> bool:
    """Пересекает ли отрезок p0→p1 прямоугольник r (слэб-метод)."""
    x0, x1, z0, z1 = r
    ax, az = p0
    bx, bz = p1
    dx, dz = bx - ax, bz - az
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, ax - x0), (dx, x1 - ax), (-dz, az - z0), (dz, z1 - az)):
        if abs(p) < 1e-9:
            if q < 0:
                return False
            continue
        r_ = q / p
        if p < 0:
            if r_ > t1:
                return False
            if r_ > t0:
                t0 = r_
        else:
            if r_ < t0:
                return False
            if r_ < t1:
                t1 = r_
    return True


def check_bounds(world: dict) -> None:
    mw, md = world["frame"]["mapGameM"]
    inside = 0
    for i in world["islands"] + world["miniIslands"]:
        x0, x1, z0, z1 = rect(i)
        if x0 < 0 or x1 > mw or z0 < 0 or z1 > md:
            fail(f"island '{i['id']}': вне карты "
                 f"x[{x0:.0f}..{x1:.0f}] z[{z0:.0f}..{z1:.0f}] "
                 f"(карта {mw:.0f}×{md:.0f} м)")
        else:
            inside += 1
    ok(f"в границах карты: {inside} из "
       f"{len(world['islands']) + len(world['miniIslands'])} объектов")


def check_overlaps(world: dict) -> None:
    all_ = world["islands"] + world["miniIslands"]
    pairs = 0
    for a in range(len(all_)):
        for b in range(a + 1, len(all_)):
            if overlap(all_[a], all_[b]):
                fail(f"island '{all_[a]['id']}' и '{all_[b]['id']}': пересекаются")
                pairs += 1
    if not pairs:
        ok(f"пересечений нет ({len(all_)} объектов, "
           f"{len(all_) * (len(all_) - 1) // 2} пар проверено)")


def check_distances(world: dict) -> None:
    by_id = {i["id"]: i for i in world["islands"]}
    s = world["frame"]["metersToStuds"]
    for m in world["miniIslands"]:
        near = min(math.hypot(m["gameXM"] - i["gameXM"], m["gameZM"] - i["gameZM"])
                   for i in world["islands"])
        if near * s < MINI_ISLAND_MIN_STUDS:
            fail(f"mini '{m['id']}': {near * s:.0f} st до ближайшего острова "
                 f"(нужно ≥ {MINI_ISLAND_MIN_STUDS} st)")
    ok(f"мини-острова: расстояния ≥ {MINI_ISLAND_MIN_STUDS} st до островов")

    isl = world["islands"]
    for a in range(len(isl)):
        for b in range(a + 1, len(isl)):
            d = math.hypot(isl[a]["gameXM"] - isl[b]["gameXM"],
                           isl[a]["gameZM"] - isl[b]["gameZM"])
            if d < ISLAND_MIN_DIST_M:
                fail(f"island '{isl[a]['id']}' и '{isl[b]['id']}': "
                     f"{d:.0f} м apart (нужно ≥ {ISLAND_MIN_DIST_M} м)")
    ok(f"острова: попарные расстояния ≥ {ISLAND_MIN_DIST_M} м")


def check_routes(world: dict) -> None:
    by_id = {i["id"]: i for i in world["islands"]}
    checked = 0
    for rid, t in world["travelTimes"].items():
        a, b = by_id.get(t["from"]), by_id.get(t["to"])
        if not a or not b:
            fail(f"route '{rid}': неизвестный остров в маршруте")
            continue
        for o in world["islands"]:
            if o["id"] in (t["from"], t["to"]):
                continue
            if seg_hits_rect((a["gameXM"], a["gameZM"]), (b["gameXM"], b["gameZM"]),
                             rect(o)):
                fail(f"route '{rid}': отрезок проходит сквозь остров '{o['name']}'")
        checked += 1
    ok(f"маршрутов проверено: {checked} (ни один не режет острова)")


def check_csv(world: dict) -> None:
    p = WORLD_DOCS / "WORLD_COORDINATES.csv"
    if not p.exists():
        fail("WORLD_COORDINATES.csv не найден")
        return
    rows = list(csv.DictReader(
        (l for l in p.read_text(encoding="utf-8").splitlines() if not l.startswith("#"))))
    if len(rows) != len(world["islands"]) + len(world["miniIslands"]):
        fail(f"CSV: {len(rows)} строк, ожидалось "
             f"{len(world['islands']) + len(world['miniIslands'])}")
    src = {i["id"]: i for i in world["islands"] + world["miniIslands"]}
    mismatch = 0
    for r in rows:
        i = src.get(r["id"])
        if not i:
            fail(f"CSV: неведомый id '{r['id']}'")
            continue
        for col, key in (("gameX", "gameXM"), ("gameZ", "gameZM"),
                         ("studsX", "studsX"), ("studsZ", "studsZ")):
            try:
                got = float(r[col])
            except (TypeError, ValueError):
                fail(f"CSV: id={r['id']} колонка {col} не число ('{r[col]}')")
                continue
            if abs(got - i[key]) > 0.51:
                fail(f"CSV: id={r['id']} {col}={got} ≠ World.json {i[key]}")
                mismatch += 1
    if not mismatch:
        ok(f"CSV == World.json: {len(rows)} строк сверено")


def check_heights(world: dict) -> None:
    H = world["frame"]["heights"]
    s = world["frame"]["metersToStuds"]
    for i in world["islands"]:
        h = i["heights"]
        if abs(i["heightM"] * H["low"] * s - h["lowY"]) > 1:
            fail(f"island '{i['id']}': lowY={h['lowY']} ≠ 0.30×высоты")
        if abs(i["heightM"] * H["plateau"] * s - h["plateauY"]) > 1:
            fail(f"island '{i['id']}': plateauY={h['plateauY']} ≠ 0.55×высоты")
        if abs(i["heightM"] * H["peak"] * s - h["peakY"]) > 1:
            fail(f"island '{i['id']}': peakY={h['peakY']} ≠ 1.00×высоты")
        if h["plateauY"] - h["lowY"] < 0.20 * i["heightM"] * s:
            fail(f"island '{i['id']}': плато−низ < 20 % игровой высоты")
    ok("высоты: низ 0.30 / плато 0.55 / пик 1.00 от высоты; Y=0 = море")


def check_capital_blocks(world: dict) -> None:
    p = GD / "arkenhold_blocks.json"
    if not p.exists():
        fail("GAME_DESIGN/arkenhold_blocks.json не найден (шаг 2.8)")
        return
    d = json.loads(p.read_text(encoding="utf-8"))
    blocks = d.get("blocks", [])
    if len(blocks) != 8:
        fail(f"кварталов Аркенхольда: {len(blocks)}, ожидалось 8")
    city_w, city_d = d.get("citySizeM", [250, 200])
    total = city_w * city_d
    area = sum(b["w"] * b["d"] for b in blocks)
    sarea = sum(s["w"] * s["d"] for s in d.get("streets", []))
    # главное: кварталы + улицы = площадь города (±10 %)
    if abs(area + sarea - total) / total > BLOCK_AREA_TOLERANCE:
        fail(f"кварталы {area:.0f} + улицы {sarea:.0f} = {area + sarea:.0f} м² "
             f"vs площадь города {total:.0f} м² — расхождение "
             f"{abs(area + sarea - total) / total * 100:.1f} % (допуск "
             f"{BLOCK_AREA_TOLERANCE * 100:.0f} %)")
    else:
        ok(f"кварталов {len(blocks)}: {area:.0f} м² ({area / total * 100:.1f} %) + "
           f"улицы {sarea:.0f} м² ({sarea / total * 100:.1f} %) = город {total:.0f} м²")
    # доля кварталов сама по себе должна быть разумной (улицы не съедают город)
    if area / total < 0.6:
        fail(f"кварталы занимают только {area / total * 100:.1f} % города — "
             f"улицы съели {sarea / total * 100:.1f} %")

    # кварталы не пересекаются и лежат в границах города
    for i, a in enumerate(blocks):
        if a["x"] < -0.01 or a["z"] < -0.01 or a["x"] + a["w"] > city_w + 0.01 \
                or a["z"] + a["d"] > city_d + 0.01:
            fail(f"квартал '{a['id']}': выходит за границы города "
                 f"({city_w}×{city_d} м)")
    for i, a in enumerate(blocks):
        for b2 in blocks[i + 1:]:
            if (a["x"] < b2["x"] + b2["w"] and b2["x"] < a["x"] + a["w"]
                    and a["z"] < b2["z"] + b2["d"] and b2["z"] < a["z"] + a["d"]):
                fail(f"кварталы '{a['id']}' и '{b2['id']}': пересекаются")
    ok(f"кварталы в границах города и не пересекаются ({len(blocks)} шт.)")

    # здания внутри кварталов, зазор ≥ 3 м, фасад к улице
    gap = d.get("grid", {}).get("buildingGapM", 3)
    for blk in blocks:
        for bl in blk.get("buildings", []):
            if bl["x"] < -0.01 or bl["z"] < -0.01 \
                    or bl["x"] + bl["w"] > blk["w"] + 0.01 \
                    or bl["z"] + bl["d"] > blk["d"] + 0.01:
                fail(f"квартал '{blk['id']}': здание {bl['kind']} "
                     f"({bl['w']}×{bl['d']}) выходит за границы квартала "
                     f"({blk['w']}×{blk['d']})")
        bs = blk.get("buildings", [])
        for i, a in enumerate(bs):
            for b2 in bs[i + 1:]:
                sep = max(a["x"] - (b2["x"] + b2["w"]), b2["x"] - (a["x"] + a["w"]))
                sepz = max(a["z"] - (b2["z"] + b2["d"]), b2["z"] - (a["z"] + a["d"]))
                if sep < gap - 0.01 and sepz < gap - 0.01:
                    fail(f"квартал '{blk['id']}': зазор между зданиями "
                         f"{a['kind']} и {b2['kind']} < {gap} м")
    nb = sum(len(b2.get("buildings", [])) for b2 in blocks)
    ok(f"зданий в кварталах: {nb}, все внутри и с зазором ≥ {gap} м")

    # причал у воды: waterfront-квартал и сам причал
    if not any(b2.get("waterfront") for b2 in blocks):
        fail("причал у воды: ни один квартал не отмечен waterfront")
    elif not any(b2.get("dock") for b2 in blocks):
        fail("причал у воды: waterfront-квартал есть, но сам причал не размещён")
    else:
        ok("причал у воды: waterfront-квартал с причалом на месте")


def main() -> None:
    world = load_world()
    check_bounds(world)
    check_overlaps(world)
    check_distances(world)
    check_routes(world)
    check_csv(world)
    check_heights(world)
    check_capital_blocks(world)

    print("=== validate_world ===")
    for n in notes:
        print("  ", n)
    if errors:
        print(f"\nWORLD FAIL — расхождений: {len(errors)}")
        for e in errors:
            print("  !!", e)
        raise SystemExit(1)
    print("\nWORLD OK")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
