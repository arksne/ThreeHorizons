# -*- coding: utf-8 -*-
"""Валидатор GAME_DESIGN (Ф1.12, ранняя версия).

Проверяет: JSON парсится, id уникальны, ссылки целостны, цепочки собраны из существующих товаров.
Запуск: python -X utf8 tools/validate_design.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / "GAME_DESIGN"

errors: list[str] = []
ok_files = 0


def load(name: str):
    p = DESIGN / name
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        globals()["ok_files"] += 1
        return data
    except json.JSONDecodeError as e:
        errors.append(f"{name}: невалидный JSON — {e}")
        return None


def unique_ids(items, where: str) -> set:
    seen = set()
    for it in items:
        i = it.get("id")
        if not i:
            errors.append(f"{where}: запись без id")
            continue
        if i in seen:
            errors.append(f"{where}: дубль id '{i}'")
        seen.add(i)
    return seen


factions = load("Factions.json")
heroes = load("Heroes.json")
goods = load("Goods.json")

faction_ids: set = set()
if factions:
    faction_ids = unique_ids(factions.get("factions", []), "Factions.factions")
    extra = factions.get("extrafactional", [])
    faction_ids |= unique_ids(extra, "Factions.extrafactional")
    for f in factions.get("factions", []) + extra:
        for key in ("specializations", "districtsGame", "paletteTokens"):
            if key in f and not isinstance(f[key], list):
                errors.append(f"Factions[{f['id']}]: {key} должен быть массивом")
        if f.get("paletteTokens") and len(f["paletteTokens"]) < 3:
            errors.append(f"Factions[{f['id']}]: слишком мало paletteTokens")

if heroes:
    unique_ids(heroes.get("heroes", []), "Heroes.heroes")
    for h in heroes.get("heroes", []):
        if faction_ids and h.get("faction") not in faction_ids:
            errors.append(f"Heroes[{h['id']}]: неизвестная фракция '{h.get('faction')}'")
        if not isinstance(h.get("age"), int):
            errors.append(f"Heroes[{h['id']}]: age должен быть числом")

if goods:
    good_ids = unique_ids(goods.get("goods", []), "Goods.goods")
    for g in goods.get("goods", []):
        for inp in g.get("inputs", []):
            if inp not in good_ids:
                errors.append(f"Goods[{g['id']}]: неизвестный вход '{inp}'")
        if g.get("tier", 0) > 0 and not g.get("inputs"):
            errors.append(f"Goods[{g['id']}]: tier>0 без inputs")
    for c in goods.get("chains", []):
        for gid in c.get("path", []):
            if gid not in good_ids:
                errors.append(f"Goods.chain[{c.get('id')}]: неизвестный товар '{gid}'")

# сводка
print(f"файлов прочитано: {ok_files}")
if errors:
    print(f"ОШИБОК: {len(errors)}")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("DESIGN OK")
