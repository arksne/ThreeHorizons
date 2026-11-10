# -*- coding: utf-8 -*-
"""Валидатор GAME_DESIGN (Ф1.12).

Проверяет: JSON парсится, id уникальны, ссылки целостны, цепочки/маршруты/квесты собраны
из существующих сущностей, ключевые константы совпадают с решениями.

Запуск:  python -X utf8 tools/validate_design.py
Негативный тест: положить в GAME_DESIGN битый .json — валидатор обязан упасть с понятной ошибкой.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / "GAME_DESIGN"

errors: list[str] = []
files: dict[str, dict] = {}


def load_all() -> None:
    for p in sorted(DESIGN.glob("*.json")):
        if p.name == "bundle.json":
            continue
        try:
            files[p.name] = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{p.name}: невалидный JSON — {e}")


def ids(items, where: str) -> set:
    seen = set()
    for it in items:
        i = it.get("id") if isinstance(it, dict) else None
        if not i:
            errors.append(f"{where}: запись без id")
            continue
        if i in seen:
            errors.append(f"{where}: дубль id '{i}'")
        seen.add(i)
    return seen


def refs(values, allowed: set, where: str) -> None:
    for v in values:
        if v not in allowed:
            errors.append(f"{where}: неизвестная ссылка '{v}'")


def main() -> None:
    load_all()
    f = files

    # --- Фракции ---
    faction_ids: set = set()
    if "Factions.json" in f:
        d = f["Factions.json"]
        faction_ids = ids(d.get("factions", []), "Factions.factions")
        faction_ids |= ids(d.get("extrafactional", []), "Factions.extrafactional")
        for x in d.get("factions", []) + d.get("extrafactional", []):
            if len(x.get("paletteTokens", [])) < 3:
                errors.append(f"Factions[{x['id']}]: меньше 3 paletteTokens")
            if not x.get("districtsGame"):
                errors.append(f"Factions[{x['id']}]: пустой districtsGame")

    # --- Герои ---
    hero_ids: set = set()
    if "Heroes.json" in f:
        heroes = f["Heroes.json"].get("heroes", [])
        hero_ids = ids(heroes, "Heroes.heroes")
        for h in heroes:
            refs([h.get("faction")], faction_ids, f"Heroes[{h['id']}].faction")
            if not isinstance(h.get("age"), int):
                errors.append(f"Heroes[{h['id']}]: age не число")

    # --- Товары ---
    good_ids: set = set()
    if "Goods.json" in f:
        d = f["Goods.json"]
        goods = d.get("goods", [])
        good_ids = ids(goods, "Goods.goods")
        for g in goods:
            refs(g.get("inputs", []), good_ids, f"Goods[{g['id']}].inputs")
            if g.get("tier", 0) > 0 and not g.get("inputs"):
                errors.append(f"Goods[{g['id']}]: tier>0 без inputs")
            if g.get("strategic") and not g.get("token"):
                errors.append(f"Goods[{g['id']}]: стратегический без token")
        for c in d.get("chains", []):
            refs(c.get("path", []), good_ids, f"Goods.chain[{c.get('id')}]")
            path = c.get("path", [])
            for a, b in zip(path, path[1:]):
                src = next((g for g in goods if g["id"] == b), None)
                if src and a not in src.get("inputs", []):
                    errors.append(f"Goods.chain[{c['id']}]: '{b}' не потребляет '{a}'")

    # --- Цены ---
    if "Prices.json" in f and "Ships.json" in f:
        prices = f["Prices.json"]
        hull_ids = {h["id"] for h in f["Ships.json"].get("hulls", [])}
        refs(list(prices.get("hulls", {}).keys()), hull_ids, "Prices.hulls")
        refs(list(prices.get("goods", {}).keys()), good_ids, "Prices.goods")

    # --- Корабли ---
    if "Ships.json" in f:
        d = f["Ships.json"]
        ids(d.get("hulls", []), "Ships.hulls")
        ids(d.get("modules", []), "Ships.modules")
        for h in d.get("hulls", []):
            if len(h.get("sizeM", [])) != 2:
                errors.append(f"Ships[{h['id']}]: sizeM должен быть [длина, ширина]")
            if h.get("triBudget", 0) > 9500:
                errors.append(f"Ships[{h['id']}]: triBudget > 9500 (лимит MeshPart)")

    # --- Профессии ---
    if "Professions.json" in f:
        skills = f["Professions.json"].get("skills", [])
        ids(skills, "Professions.skills")
        for s in skills:
            lvls = s.get("levels", [])
            hours = [l.get("hours", 0) for l in lvls]
            if hours != sorted(hours) or not hours:
                errors.append(f"Professions[{s['id']}]: уровни должны расти по часам")

    # --- Здания ---
    if "Buildings.json" in f:
        b = f["Buildings.json"].get("classes", [])
        ids(b, "Buildings.classes")
        for x in b:
            if len(x.get("sizeM", [])) != 2:
                errors.append(f"Buildings[{x['id']}]: sizeM должен быть [ширина, глубина]")

    # --- Маршруты ---
    if "Routes.json" in f:
        routes = f["Routes.json"].get("routes", [])
        ids(routes, "Routes.routes")
        for r in routes:
            refs([r.get("from"), r.get("to")], faction_ids, f"Routes[{r['id']}]")
            if r.get("type") not in ("cargo", "contraband"):
                errors.append(f"Routes[{r['id']}]: type должен быть cargo/contraband")

    # --- Погода ---
    if "Weather.json" in f:
        states = f["Weather.json"].get("states", [])
        ids(states, "Weather.states")
        for s in states:
            for key in ("visibilityMultiplier", "wearMultiplier"):
                if key not in s.get("effects", {}):
                    errors.append(f"Weather[{s['id']}]: нет effect.{key}")

    # --- NPC и квесты ---
    npc_ids: set = set()
    if "NPC.json" in f:
        npcs = f["NPC.json"].get("npcs", [])
        npc_ids = ids(npcs, "NPC.npcs")
        for n in npcs:
            if len(n.get("schedule", {})) < 3:
                errors.append(f"NPC[{n['id']}]: расписание меньше 3 состояний")
    if "Quests.json" in f:
        quests = f["Quests.json"].get("quests", [])
        ids(quests, "Quests.quests")
        for q in quests:
            refs([q.get("hero")], hero_ids, f"Quests[{q['id']}].hero")
            refs([q.get("giver")], npc_ids, f"Quests[{q['id']}].giver")
            if not q.get("txIdRule"):
                errors.append(f"Quests[{q['id']}]: нет txIdRule")

    # --- Константы ---
    if "constants.json" in f:
        c = f["constants.json"]
        if c.get("scale", {}).get("metersToStuds") != 3.571:
            errors.append("constants.scale.metersToStuds должен быть 3.571 (S-01)")
        if c.get("scale", {}).get("worldCompression") != 0.1:
            errors.append("constants.scale.worldCompression должен быть 0.1 (S-02)")
        if c.get("limits", {}).get("playersPerShard") != 60:
            errors.append("constants.limits.playersPerShard должен быть 60 (S-04)")

    # --- generatedFrom: все источники должны существовать ---
    for name, data in files.items():
        for src in data.get("generatedFrom", []) or []:
            path = ROOT / src.split("#")[0].strip()
            if not path.exists():
                errors.append(f"{name}: generatedFrom ссылается на несуществующий файл "
                              f"«{src}»")

    # --- итог ---
    print(f"файлов: {len(f)} | " + ", ".join(sorted(files)))
    if errors:
        print(f"ОШИБОК: {len(errors)}")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("DESIGN OK")


if __name__ == "__main__":
    main()
