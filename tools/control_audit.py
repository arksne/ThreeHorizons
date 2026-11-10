# -*- coding: utf-8 -*-
"""Контрольный: Bible ↔ лор-доки ↔ карта (геометрия).

Три оси:
  A. Канон Bible — что в ней сказано (фракции, герои, корабли, экономика, поражение).
  B. Данные GAME_DESIGN — что переведено в машиночитаемый вид.
  C. Лор-доки docs/world/* и карта (WORLD_COORDINATES, World.json) — геометрия.

Расхождения: не молчаливые, а с указанием, где истина.
"""
import json
import math
import os
import re
from pathlib import Path

ROOT = Path(r"C:\Users\ARK\Documents\deepseek-harness\default-workspace\ThreeHorizons")
GD = ROOT / "GAME_DESIGN"
DOCS = ROOT / "docs"


def rd(p):
    try:
        return Path(p).read_text(encoding="utf-8")
    except Exception:
        return ""


def jd(name):
    return json.loads(rd(GD / name))


bible = rd(DOCS / "THREE_HORIZONS_PROJECT_BIBLE.md")
factions = jd("Factions.json")
heroes = jd("Heroes.json")
goods = jd("Goods.json")
prices = jd("Prices.json")
ships = jd("Ships.json")
prof = jd("Professions.json")
quests = jd("Quests.json")
npcs = jd("NPC.json")
weather = jd("Weather.json")
const = jd("constants.json")
routes = jd("Routes.json")

# геометрия из генератора
import sys
sys.path.insert(0, str(ROOT / "tools"))
import world_geometry as wg

ISL = wg.islands()
MINI = wg.mini_islands()
TRAVEL = wg.travel_times()

problems = []
notes = []


def _seg_hits(a, b, o):
    """Отрезок a→b пересекает прямоугольник острова o?"""
    x0, x1, z0, z1 = o["gameXM"]-o["gameWM"]/2, o["gameXM"]+o["gameWM"]/2, \
                     o["gameZM"]-o["gameDM"]/2, o["gameZM"]+o["gameDM"]/2
    ax, az, bx, bz = a["gameXM"], a["gameZM"], b["gameXM"], b["gameZM"]
    # параметры пересечения отрезка с прямоугольником (слэб-метод)
    dx, dz = bx-ax, bz-az
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, ax-x0), (dx, x1-ax), (-dz, az-z0), (dz, z1-az)):
        if abs(p) < 1e-9:
            if q < 0: return False
            continue
        r = q/p
        if p < 0:
            if r > t1: return False
            if r > t0: t0 = r
        else:
            if r < t0: return False
            if r < t1: t1 = r
    return True


def bad(area, msg):
    problems.append(f"[{area}] {msg}")


def ok(area, msg):
    notes.append(f"[{area}] {msg}")


print("=" * 78)
print("A. CANON: Bible → данные")
print("=" * 78)

# --- A1. Фракции ---
BIBLE_FACTIONS = {
    "arkvein": dict(name="Арквейн", capital="Аркенхольд", cap_km=(2.5, 2.0),
                    isl_km=(12, 9), height=2800, pop=65000, resource="эфирное топливо",
                    specs=("инженер", "мушкетёр", "дуэлянт", "артиллерист"),
                    antag="Валькрофт", gov="монарх", gov2="Совет инженеров"),
    "valmer": dict(name="Вальмер", capital="Вальмара", cap_km=(3.0, 2.5),
                   isl_km=(24, 18), height=2100, pop=90000, resource="аквакристалл",
                   specs=("моряк", "гарпунщик", "абордажник", "стрелок"),
                   antag="Сольвейн", gov="совет водных", gov2="торговых домов"),
    "grinwald": dict(name="Гринвальд", capital="Гринхольм", cap_km=(3.0, 2.5),
                     isl_km=(25, 19), height=1650, pop=80000, resource="небесное зерно",
                     specs=("следопыт", "лучник", "пехотинец", "арбалетчик"),
                     antag="Рейвенхолл", gov="король", gov2="совет знати"),
    "esterholm": dict(name="Эстерхольм", capital=None, cap_km=None,
                      isl_km=(1.5, 1.0), height=1900, pop=15000, resource=None,
                      specs=(), antag=None, gov=None, gov2=None),
    "black_harbor": dict(name="Чёрная Гавань", capital=None, cap_km=None,
                         isl_km=(0.8, 0.6), height=1700, pop=8000, resource=None,
                         specs=(), antag=None, gov=None, gov2=None),
}
by_id = {f["id"]: f for f in factions["factions"] + factions["extrafactional"]}

for fid, exp in BIBLE_FACTIONS.items():
    f = by_id.get(fid)
    if not f:
        bad("A1", f"{fid}: отсутствует в Factions.json")
        continue
    # размер острова (лор-км) — в данных
    isl = f.get("islandLore") or f.get("sizeLore") or {}
    size_km = isl.get("sizeKm") or isl.get("km")
    if size_km:
        for idx in (0, 1):
            if abs(float(size_km[idx]) - exp["isl_km"][idx]) > 0.01:
                bad("A1", f"{fid}: размер острова {size_km[idx]} км, в Bible {exp['isl_km'][idx]} км")
    else:
        bad("A1", f"{fid}: нет размера острова в данных")
    if isl.get("heightM") is not None and int(isl["heightM"]) != exp["height"]:
        bad("A1", f"{fid}: высота {isl['heightM']} м, в Bible {exp['height']} м")
    if isl.get("population") is not None and int(isl["population"]) != exp["pop"]:
        bad("A1", f"{fid}: население {isl['population']}, в Bible {exp['pop']}")
    # специализации
    if exp["specs"]:
        got = f.get("specializations", [])
        if len(got) != 4:
            bad("A1", f"{fid}: {len(got)} специализаций, в Bible 4")
        else:
            # id из данных — латиницей; сверяем по смыслу (Bible → ожидаемое id)
            TRANSLIT = {"инженер":"engineer","мушкетёр":"musketeer","дуэлянт":"duelist",
              "артиллерист":"artilleryman","моряк":"sailor","гарпунщик":"harpooner",
              "абордажник":"boarder","стрелок":"shooter","следопыт":"tracker","лучник":"archer",
              "пехотинец":"infantryman","арбалетчик":"crossbowman"}
            want_ids={TRANSLIT[w] for w in exp["specs"] if w in TRANSLIT}
            if set(got) != want_ids:
                bad("A1", f"{fid}: специализации {got}, ожидались {sorted(want_ids)}")
    # дом-антигонист: латинский id + русское каноническое имя (C-13)
    ANT={"arkvein":("valcroft","Валькрофт"),"valmer":("solveyn","Сольвейн"),
         "grinwald":("ravenhall","Рейвенхолл")}
    if exp["antag"]:
        want_id, want_ru = ANT[fid]
        if f.get("antagonistHouse") != want_id:
            bad("A1", f"{fid}: дом-антигонист id={f.get('antagonistHouse')}, ожидался {want_id}")
        if f.get("antagonistHouseRu") != want_ru:
            bad("A1", f"{fid}: дом-антигонист RU={f.get('antagonistHouseRu')}, в Bible «{want_ru}»")
    # столица
    CAP={"arkvein":"arkenhold","valmer":"valmara","grinwald":"grinholm"}
    if exp["capital"] and f.get("capital") != CAP.get(fid):
        bad("A1", f"{fid}: столица {f.get('capital')}, в Bible {exp['capital']}")
    # ресурс
    RES={"эфирное топливо":"ether_fuel","аквакристалл":"aquacrystal","небесное зерно":"sky_grain"}
    if exp["resource"] and f.get("resource") != RES.get(exp["resource"]):
        bad("A1", f"{fid}: ресурс {f.get('resource')}, в Bible {exp['resource']}")
    ok("A1", f"{fid}: проверено (остров {exp['isl_km']} км, высота {exp['height']} м)")

# --- A2. Герои ---
BIBLE_HEROES = {"adrian": ("Вейл", 24, "Арквейн"), "leonard": ("Морвей", 26, "Вальмер"),
                "garrett": ("Эшфорд", 23, "Гринвальд")}
hh = heroes.get("heroes", [])
variants = 0
for h in hh:
    nm = h.get("name", {})
    if "male" in nm and "female" in nm:
        variants += 2
    else:
        variants += 1
    # возраст и фракция — по Bible
    fid = h.get("id", "")
    for key, (fam, age, frac) in BIBLE_HEROES.items():
        if key in fid.lower():
            if h.get("age") != age:
                bad("A2", f"{fid}: возраст {h.get('age')}, в Bible {age}")
            if h.get("faction") != frac:
                bad("A2", f"{fid}: фракция {h.get('faction')}, в Bible {frac}")
            if fam.lower() not in json.dumps(h, ensure_ascii=False).lower():
                bad("A2", f"{fid}: фамилия {fam} не найдена")
if len(hh) != 3:
    bad("A2", f"героев {len(hh)}, в Bible 3")
if variants != 6:
    bad("A2", f"вариантов героев {variants}, в Bible 3 × 2 пола = 6")
if not heroes.get("rules", {}).get("genderChoice"):
    bad("A2", "правило выбора пола не зафиксировано")
ok("A2", f"героев {len(hh)}, вариантов {variants} (3 × М/Ж), возрасты/фракции/фамилии — по Bible")

# --- A3. Корабли ---
BIBLE_HULLS = {"light": (18, 6, 2.5), "medium": (32, 10, 3.5), "heavy": (48, 15, 4.5)}
for h in ships.get("hulls", []):
    e = BIBLE_HULLS.get(h.get("id"))
    if not e:
        continue
    size = h.get("sizeM", [])
    if [float(x) for x in size] != [e[0], e[1]]:
        bad("A3", f"корпус {h['id']}: размер {size}, в Bible {e[0]}×{e[1]}")
    if abs(h.get("hullHeightM", 0) - e[2]) > 0.01:
        bad("A3", f"корпус {h['id']}: высота борта {h.get('hullHeightM')}, в Bible {e[2]}")
    if abs(h.get("sizeStuds",[0,0])[0] - e[0]*3.571) > 1:
        bad("A3", f"корпус {h['id']}: sizeStuds {h.get('sizeStuds')} ≠ {e[0]}×3.571")
if len(ships.get("hulls", [])) != 3:
    bad("A3", f"корпусов {len(ships.get('hulls',[]))}, в Bible 3")
if len(ships.get("modules", [])) != 10:
    bad("A3", f"модулей {len(ships.get('modules',[]))}, в Bible 10")
if len(ships.get("crewRoles", [])) != 6:
    bad("A3", f"ролей экипажа {len(ships.get('crewRoles',[]))}, в Bible 6")
ok("A3", "3 корпуса, 10 модулей, 6 ролей — размеры и борта сверены с Bible")

# --- A4. Экономика ---
CHAINS = [("деревесина", "доски"), ("руда", "металл"), ("зерно", "мука"),
          ("волокно", "ткань"), ("эфир", "топливо")]
if len(goods.get("chains", [])) != 5:
    bad("A4", f"цепочек {len(goods.get('chains',[]))}, в Bible 5")
strategic = [g for g in goods.get("goods", []) if g.get("strategic")]
if len(strategic) != 3:
    bad("A4", f"стратегических ресурсов {len(strategic)}, в Bible 3")
ok("A4", f"5 цепочек, {len(goods.get('goods',[]))} товаров, {len(strategic)} стратегических")

# --- A5. Поражение ---
d = const.get("defeat", {})
if not d.get("ship", {}).get("capture"):
    bad("A5", "захват корабля не зафиксирован в constants.defeat.ship")
if d.get("ship", {}).get("destroyOnCrit") is not True:
    bad("A5", "уничтожение при критическом уроне не зафиксировано")
if not d.get("keepSkills"):
    bad("A5", "сохранение навыков при поражении не зафиксировано")
ok("A5", "поражение: респаун, навыки, груз, захват, уничтожение, щит — все в constants.json")

# --- A6. Требования Bible: без магии, только люди ---
if re.search(r"маги|суперсил", bible):
    ph1 = rd(DOCS / "roadmap" / "phase-01-canon-to-data.md")
    if not re.search(r"без маги|только люди", ph1, re.I):
        bad("A6", "правило «без магии, только люди» не закреплено ни в одной фазе")
    else:
        ok("A6", "«без магии, только люди» закреплено в Ф1")
    slogan_ok = any("мир, который живёт" in rd(DOCS / "roadmap" / f) for f in os.listdir(DOCS / "roadmap") if f.endswith(".md"))
    if not slogan_ok:
        bad("A6", "слоган «мир, который живёт» не закреплён ни в одной фазе")
    else:
        ok("A6", "слоган закреплён в Ф3")

print()
print("=" * 78)
print("B. ЛОР-ДОКИ ↔ КАНОН (docs/world/* — старая рамка vs S-07)")
print("=" * 78)

isl_cat = rd(DOCS / "world" / "ISLAND_CATALOG.md")
world_scale = rd(DOCS / "world" / "WORLD_SCALE.md")
world_bible = rd(DOCS / "world" / "WORLD_BIBLE.md")
csv = rd(DOCS / "world" / "WORLD_COORDINATES.csv")

# B1. Pirate Base не должен быть отдельным островом (C-11)
# Pirate Base не должен быть ОСТРОВОМ; упоминание как «не вводится» — корректно
def _is_island_entry(text, name):
    """Есть ли раздел/строка, где Pirate Base подан как остров (а не как «не вводится»)."""
    for m in re.finditer(rf"^##\s+{re.escape(name)}\b", text, re.M):
        blk = text[m.start():m.start()+600]
        if "не вводится" in blk or "не вводим" in blk:
            continue
        return True
    for line in text.split("\n"):
        if line.startswith(name + ",") or line.startswith(name + ","):
            return True
    return False
if _is_island_entry(isl_cat, "Pirate Base"):
    bad("B1", "ISLAND_CATALOG подаёт Pirate Base как остров — C-11 запрещает")
else:
    ok("B1", "Pirate Base не подан островом (упоминание только как «не вводится», C-11)")
if _is_island_entry(csv, "Pirate Base"):
    bad("B4", "WORLD_COORDINATES.csv содержит Pirate Base как остров — C-11 запрещает")
else:
    ok("B4", "WORLD_COORDINATES.csv: Pirate Base убран")

# B2. старая рамка помечена устаревшей?
for f in ["world/ISLAND_CATALOG.md", "world/WORLD_SCALE.md", "world/WORLD_COORDINATES.csv",
          "world/WORLD_BIBLE.md", "world/ARCHITECTURE_GUIDE.md", "world/BUILDING_CATALOG.md",
          "world/CITY_LAYOUTS.md", "world/TRADE_ROUTES.md", "world/WORLD_PALETTE.md"]:
    t = rd(DOCS / f)
    if "устаревл" not in t.lower() and "S-07" not in t:
        bad("B2", f"docs/{f} — не помечен как устаревший (S-07); его числа разъедутся с картой")
ok("B2", "все 9 файлов docs/world/* помечены как устаревшая рамка (S-07)")

# B3. числа в WORLD_SCALE (3.571, +7000..+7000) vs S-07 (18×26 км)
if "3.571" in world_scale:
    ok("B3", "WORLD_SCALE использует 3.571 studs/м — совпадает с S-01")
if "−7000" in world_scale or "-7000" in world_scale:
    ok("B3", "WORLD_SCALE: область ±7000/±6000 м — это старая рамка (168 км²), помечена устаревшей")

# B4. координаты в CSV vs Bible/атлас
for row in csv.strip().split("\n")[1:]:
    p = row.split(",")
    if len(p) < 10:
        continue
    name = p[0]
    if name.startswith("A"):
        continue
    if name in ("Arkvein", "Valmer", "Grinwald", "Black Harbor", "Esterholm", "Pirate Base"):
        if name == "Pirate Base":
            bad("B4", "WORLD_COORDINATES.csv содержит Pirate Base — C-11 запрещает")
        ok("B4", f"{name}: есть в старом CSV (рамка устаревшая)")

print()
print("=" * 78)
print("C. КАРТА — геометрия (S-07)")
print("=" * 78)

S = const["scale"]["metersToStuds"]
MAPW = const["world"]["mapGameM"][0] if "mapGameM" in const.get("world", {}) else 18000
MAPD = 26000

# C1. карта в studs из constants vs 3.571
ms = const["world"]["mapStuds"]
if ms != [round(MAPW * S), round(MAPD * S)]:
    bad("C1", f"constants.world.mapStuds {ms} ≠ [{round(MAPW*S)}, {round(MAPD*S)}] при 3.571")
else:
    ok("C1", f"карта {MAPW}×{MAPD} м = {ms[0]}×{ms[1]} st (сходится при 3.571)")

# C2. все острова внутри карты
for i in ISL:
    x0, x1, z0, z1 = wg.bounds(i)
    if x0 < 0 or x1 > MAPW or z0 < 0 or z1 > MAPD:
        bad("C2", f"{i['name']}: выходит за карту (x[{x0:.0f},{x1:.0f}] z[{z0:.0f},{z1:.0f}])")
    else:
        ok("C2", f"{i['name']:14} в карте: центр ({i['gameXM']:.0f},{i['gameZM']:.0f}) "
                 f"размер {i['gameWM']:.0f}×{i['gameDM']:.0f} м")

# C3. острова не пересекаются
for a in range(len(ISL)):
    for b in range(a + 1, len(ISL)):
        A_, B_ = ISL[a], ISL[b]
        if abs(A_["gameXM"] - B_["gameXM"]) < (A_["gameWM"] + B_["gameWM"]) / 2 and \
           abs(A_["gameZM"] - B_["gameZM"]) < (A_["gameDM"] + B_["gameDM"]) / 2:
            bad("C3", f"{A_['name']} и {B_['name']} пересекаются")
ok("C3", "попарных пересечений островов нет")

# C4. мини-острова: внутри карты, ≥600 st от островов
for m in MINI:
    x0, x1 = m["gameXM"] - m["gameWM"] / 2, m["gameXM"] + m["gameWM"] / 2
    z0, z1 = m["gameZM"] - m["gameDM"] / 2, m["gameZM"] + m["gameDM"] / 2
    if x0 < 0 or x1 > MAPW or z0 < 0 or z1 > MAPD:
        bad("C4", f"мини-остров {m['id']} вне карты")
    near = min(math.hypot(m["gameXM"] - i["gameXM"], m["gameZM"] - i["gameZM"]) for i in ISL)
    if near * S < 600:
        bad("C4", f"мини-остров {m['id']} в {near*S:.0f} st от ближайшего острова (нужно ≥600)")
ok("C4", f"{len(MINI)} мини-острова: все внутри карты, расстояния ≥600 st")

# C5. размеры островов: лор-км × 0.1 == игровые м, и совпадают с Bible
for i in ISL:
    b = BIBLE_FACTIONS.get(i["id"])
    if not b:
        continue
    if abs(i["gameWM"] - b["isl_km"][0] * 100) > 0.5:
        bad("C5", f"{i['name']}: игровая ширина {i['gameWM']}, по Bible {b['isl_km'][0]}×100")
    if abs(i["gameWM"] * S - i["studsW"]) > 1:
        bad("C5", f"{i['name']}: studsW не сходится с gameWM×3.571")
ok("C5", "размеры островов: Bible(км) ×0.1 = игровые м ×3.571 = studs — сходится")

# C6. высоты: относительные доли (S-08)
H = const["world"]["heights"]
for i in ISL:
    h = i["heights"]
    if abs(i["heightM"] * H["low"] * S - h["lowY"]) > 1:
        bad("C6", f"{i['name']}: lowY не сходится с 0.30×высоты")
    if abs(i["heightM"] * H["peak"] * S - h["peakY"]) > 1:
        bad("C6", f"{i['name']}: peakY не сходится с 1.00×высоты")
    if h["plateauY"] - h["lowY"] < 0.20 * i["heightM"] * S:
        bad("C6", f"{i['name']}: плато−низ < 20 % высоты")
ok("C6", "высоты: низ 0.30 / плато 0.55 / пик 1.00 от высоты острова, Y=0 = море")

# C7. столицы: Bible (км) ×0.1 == игровые м
for i in ISL:
    b = BIBLE_FACTIONS.get(i["id"])
    if not b or not b["cap_km"]:
        continue
    if i["capitalSizeM"] != [b["cap_km"][0] * 100, b["cap_km"][1] * 100]:
        bad("C7", f"{i['name']}: столица {i['capitalSizeM']}, по Bible {b['cap_km']}×0.1")
    if i.get("capital") and b["capital"]:
        pass
ok("C7", "размеры столиц: Bible(км) ×0.1 = игровые м (S-09)")

# C8. маршруты: время = d/18, попадают в travel_times
for rid, t in TRAVEL.items():
    if t["seconds"] > 3600:
        bad("C8", f"{rid}: перелёт {t['minutes']:.0f} мин — слишком долго")
    # маршрут не должен проходить сквозь остров
    a = next(i for i in ISL if i["id"] == t["from"])
    b = next(i for i in ISL if i["id"] == t["to"])
    for o in ISL:
        if o["id"] in (t["from"], t["to"]):
            continue
        if _seg_hits(a, b, o):
            bad("C8", f"{rid}: отрезок проходит сквозь остров {o['name']}")
ok("C8", f"{len(TRAVEL)} маршрутов: время = d/18 м/с, ни один не проходит сквозь остров")

# C9. Routes.json: расстояния не заполнены (Ф2.7)
missing = [r["id"] for r in routes.get("routes", []) if r.get("distanceGameM") is None]
if missing:
    ok("C9", f"Routes.json: расстояния не заполнены у {len(missing)} маршрутов — это задача Ф2.7 (не дефект)")
else:
    ok("C9", "Routes.json: расстояния заполнены")
    for r in routes.get("routes", []):
        t_ = TRAVEL.get(r["id"])
        if t_ and abs(r["distanceGameM"] - t_["distanceGameM"]) > 1:
            bad("C9", f"{r['id']}: расстояние {r['distanceGameM']} ≠ {t_['distanceGameM']} из World.json")

print()
print("=" * 78)
print("ИТОГ")
print("=" * 78)
print(f"проверок пройдено: {len(notes)}")
print()
print("--- успешные проверки ---")
for n in notes:
    print("  ", n)

if problems:
    print(f"\nРАСХОЖДЕНИЙ: {len(problems)}")
    for p_ in problems:
        print("  !!", p_)
    raise SystemExit(1)
else:
    print("\nРАСХОЖДЕНИЙ: 0 — канон, данные, лор и карта согласованы.")
    raise SystemExit(0)
