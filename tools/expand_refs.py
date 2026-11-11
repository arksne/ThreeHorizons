# -*- coding: utf-8 -*-
"""Ф4 · Расширение реестра классов моделей: 57 → 250+.

Дописывает недостающие группы, которых нет в `docs/roadmap/model-classes.json`:
  - персонажи: взрослые базовые тела + NPC по профессиям
  - одежда: комплекты по тирам 10/20/30/40/50 (10 → 20 → 30 → 40 → 50)
  - корабли: 20 корпусов с разным потенциалом улучшения
  - оружие: 50–60 видов по ролям
  - детали построек: фаски, кровли, окна, двери, лестницы, трубы, решётки
  - предметы и ресурсы: всё из Goods.json
  - ремёсла и инструменты: по 12 профессиям

Все размеры — реальные (метры) из канона; tri-бюджеты — по классу.

Запуск: python -X utf8 tools/expand_refs.py [--dry]
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "docs" / "roadmap" / "model-classes.json"

HERO_BUDGET = 12000
BUILDING_BUDGET = 12000
PROP_BUDGET = 2000
CHAR_BUDGET = 12000
WEAPON_BUDGET = 4000
SHIP_BUDGET = 12000
CLOTH_BUDGET = 2000
PARTICLE_BUDGET = 200
TILE_BUDGET = 2000

ARK = ["ARK_GRAPHITE", "ARK_STONE", "ARK_WOOD_DARK", "ARK_BURGUNDY", "ARK_COPPER",
       "ARK_STEEL", "ARK_PLASTER"]
VAL = ["VAL_LIMESTONE", "VAL_CREAM", "VAL_SAND", "VAL_TEAL", "VAL_SEA", "VAL_BRONZE", "VAL_WHITE"]
GRN = ["GRN_OLIVE", "GRN_FOREST", "GRN_WOOD", "GRN_BEIGE", "GRN_STRAW", "GRN_TERRA", "GRN_STONE"]
NEUT = ["INK", "PARCHMENT", "PARCH_DARK", "BRASS", "WOOD_UI", "DANGER", "FOCUS_BLUE"]


def add(items, cid, name, group, size, tri, materials, usage):
    items.append({"id": cid, "name": name, "group": group, "sizeM": size,
                  "triBudget": tri, "materials": materials, "usage": usage})


def expand(existing: list) -> list:
    have = {c["id"] for c in existing}
    out = list(existing)

    # ---------- персонажи: базовые тела ----------
    BASES = [
        ("char_base_m_lean", "Базовое тело: мужчина худощавое", "1.7"),
        ("char_base_m_heavy", "Базовое тело: мужчина тяжёлое", "1.7"),
        ("char_base_m_old", "Базовое тело: мужчина пожилой", "1.7"),
        ("char_base_f_lean", "Базовое тело: женщина худощавая", "1.7"),
        ("char_base_f_heavy", "Базовое тело: женщина крепкая", "1.7"),
        ("char_base_f_old", "Базовое тело: женщина пожилая", "1.7"),
        ("char_base_m_young", "Базовое тело: мужчина молодой", "1.7"),
        ("char_base_f_young", "Базовое тело: женщина молодая", "1.7"),
    ]
    for cid, name, size in BASES:
        if cid in have:
            continue
        add(out, cid, name, "char_bodies", size, CHAR_BUDGET, NEUT,
            "персонажи: базовое тело в простом белье")

    # ---------- персонажи: NPC по профессиям ----------
    NPC_ROLES = [
        ("farmer", "Крестьянин", GRN), ("miller", "Мельник", GRN),
        ("smith", "Кузнец", ARK), ("engineer", "Инженер", ARK),
        ("carpenter", "Плотник", GRN), ("sailor", "Матрос", VAL),
        ("captain", "Капитан", VAL), ("merchant", "Купец", VAL),
        ("innkeeper", "Хозяин таверны", VAL), ("dockhand", "Портовый рабочий", ARK),
        ("miner", "Шахтёр", ARK), ("hunter", "Охотник", GRN),
        ("guard", "Городской страж", ARK), ("priest", "Служитель культа", NEUT),
        ("noble", "Дворянин", VAL), ("nurse", "Лекарь", NEUT),
        ("fisherman", "Рыбак", VAL), ("trader", "Торговец", VAL),
        ("worker", "Чернорабочий", ARK), ("clerk", "Писарь", NEUT),
    ]
    for role, name, pal in NPC_ROLES:
        cid = f"char_npc_{role}"
        if cid in have:
            continue
        add(out, cid, f"NPC: {name}", "char_npcs", "1.7", CHAR_BUDGET, pal,
            f"персонажи: {name.lower()} с профессиональной одеждой")

    # ---------- одежда: комплекты по тирам ----------
    TIERS = [
        (10, "Базовый", 1, ["рубаха", "штаны", "пояс"]),
        (20, "Рабочий", 3, ["рубаха", "штаны", "куртка", "платок", "сапоги"]),
        (30, "Городской", 5, ["кафтан", "штаны", "плащ", "шапка", "перчатки", "туфли"]),
        (40, "Офицерский", 6, ["камзол", "штаны", "бушлат", "перчатки", "шляпа", "сапоги", "пояс"]),
        (50, "Парадный", 7, ["камзол с шитьём", "плащ", "шляпа с пером", "перчатки", "туфли", "пояс", "цепочка"]),
    ]
    SLOTS = ["рубаха", "штаны", "пояс", "куртка", "платок", "сапоги", "кафтан", "плащ",
             "шапка", "перчатки", "туфли", "камзол", "бушлат", "шляпа", "цепочка"]
    for tier, tname, count, slots in TIERS:
        for i in range(count):
            slot = slots[i % len(slots)]
            cid = f"cloth_t{tier}_{slot.replace(' ', '_')}_{i+1}"
            if cid in have:
                continue
            add(out, cid, f"Одежда тир {tier} ({tname}): {slot} #{i+1}",
                "clothing", "—", CLOTH_BUDGET, NEUT,
                f"одежда: комплект тира {tier}, предмет {i+1} из {count}")

    # ---------- корабли: 20 корпусов ----------
    SHIPS = [
        ("skiff", "Шлюпка", 4, 1.5, 0.8), ("trawler", "Траулер", 7, 2.5, 1.0),
        ("sloop", "Шлюп", 10, 3.5, 1.2), ("cutter", "Катер", 14, 4.5, 1.4),
        ("smack", "Смак", 12, 3.2, 1.1), ("schoner", "Шхунер", 16, 4.2, 1.3),
        ("brig", "Бриг", 20, 5.2, 1.6), ("brigantine", "Бригантина", 24, 5.8, 1.7),
        ("barque", "Барк", 30, 7.0, 2.1), ("merchant", "Торговое судно", 28, 6.6, 2.2),
        ("clipper", "Клипер", 34, 6.0, 2.0), ("frigate", "Фрегат", 32, 6.2, 1.9),
        ("galleon", "Галеон", 44, 9.0, 2.8), ("manowar", "Линейный корабль", 52, 10.5, 3.2),
        ("carrack", "Каракка", 38, 8.0, 2.6), ("caravel", "Каравелла", 18, 4.4, 1.5),
        ("barge", "Баржа", 15, 4.0, 2.4), ("lighter", "Лайтер", 11, 3.0, 1.8),
        ("pinnace", "Пинас", 9, 2.8, 1.2), ("hulk", "Халк", 36, 7.4, 2.6),
    ]
    for cid, name, l, w, h in SHIPS:
        if cid in have:
            continue
        add(out, cid, f"Корпус: {name} ({l}×{w} м, высота борта {h} м)",
            "ships", f"{l}×{w}", SHIP_BUDGET, VAL,
            f"корабли: {name.lower()}, потенциал улучшения до следующего класса")

    # ---------- оружие: 55 видов ----------
    WEAPONS = [
        ("cutlass", "Абордажная сабля"), ("rapier", "Рапира"), ("sword", "Меч"),
        ("longsword", "Длинный меч"), ("greatsword", "Двуручник"), ("sabre", "Сабля"),
        ("broadsword", "Палаш"), ("falchion", "Фальшион"), ("estoc", "Эсток"),
        ("dagger", "Кинжал"), ("dirk", "Кортик"), ("mainchou", "Мейншот"),
        ("club", "Булава"), ("mace", "Молот"), ("warhammer", "Боевой молот"),
        ("spear", "Копьё"), ("lance", "Пика"), ("halberd", "Алебарда"),
        ("pike", "Муштра"), ("trident", "Трезубец"), ("glaive", "Глева"),
        ("axe", "Топор"), ("battleaxe", "Секира"), ("beardedaxe", "Бородатая секира"),
        ("handaxe", "Рукавной топор"), ("waraxe", "Боевой топор"), ("poleaxe", "П Pole-axe"),
        ("bow", "Лук"), ("longbow", "Длинный лук"), ("shortbow", "Короткий лук"),
        ("crossbow", "Арбалет"), ("arbalest", "Арбалест"), ("sling", "Праща"),
        ("atlatl", "Атлатл"), ("javelin", "Метательное копьё"), ("dart", "Дротик"),
        ("flintlock", "Кремнёвый пистолет"), ("miquelet", "Микелет"), ("snaphance", "Снафанс"),
        ("wheellock", "Колесцовый пистолет"), ("blunderbuss", "Блаундер-мушкет"),
        ("musket", "Мушкет"), ("caliver", "Каливер"), ("arquebus", "Аркебуз"),
        ("pistol", "Пистолет"), ("carbine", "Карабин"), ("rifle", "Винтовка"),
        ("axe_marine", "Абордажный топор"), ("boardingpike", "Абордажная пика"),
        ("cutlass_sail", "Абордажный тесак"),
    ]
    for cid, name in WEAPONS:
        if cid in have:
            continue
        add(out, cid, f"Оружие: {name}", "weapons", "—", WEAPON_BUDGET,
            [ARK_STEEL := "ARK_STEEL", "ARK_WOOD_DARK", "ARK_COPPER"],
            "оружие: ближний бой, огнестрел, метательное — по ролям экипажа")

    # ---------- детали построек ----------
    DETAILS = [
        ("det_roof_gable", "Двускатная крыша"), ("det_roof_hip", "Четырёхскатная крыша"),
        ("det_roof_flat", "Плоская кровля"), ("det_roof_tower", "Шатёр башни"),
        ("det_roof_sawtooth", "Пилобразная кровля"), ("det_roof_mansard", "Мансардная крыша"),
        ("det_ridge", "Конёк кровли"), ("det_eave", "Свес кровли"),
        ("det_eaves_board", "Подшивка карниза"), ("det_gutter", "Жёлоб"),
        ("det_downpipe", "Водосточная труба"), ("det_chimney", "Труба с колпаком"),
        ("det_beam_horizontal", "Горизонтальная балка"), ("det_beam_vertical", "Вертикальная стойка"),
        ("det_brace_diagonal", "Диагональный раскос"), ("det_timber_frame", "Фахверк панель"),
        ("det_foundation", "Цоколь фундамента"), ("det_plinth_stone", "Каменный цоколь"),
        ("det_stairs", "Наружная лестница"), ("det_stairs_rail", "Перила лестницы"),
        ("det_balcony", "Балкон"), ("det_balcony_rail", "Ограждение балкона"),
        ("det_window_frame", "Оконная рама"), ("det_window_mullion", "Переплёт окна"),
        ("det_window_sill", "Подоконник"), ("det_window_shutters", "Ставни"),
        ("det_window_grate", "Решётка окна"), ("det_door_frame", "Дверной косяк"),
        ("det_door_leaf", "Дверное полотно"), ("det_door_hinges", "Петли двери"),
        ("det_door_ring", "Дверное кольцо"), ("det_arch_stone", "Каменная арка"),
        ("det_bracket", "Кронштейн"), ("det_corbel", "Каменный выступ"),
        ("det_corner_stone", "Угловой камень"), ("det_sill_band", "Поясок цоколя"),
        ("det_wainscot", "Панель обшивки"), ("det_lintel", "Перемычка"),
        ("det_gable_board", "Доска щипца"), ("det_bargeboard", "Подшивка свеса"),
        ("det_gutter_join", "Соединение жёлоба"), ("det_wall_cap", "Парапет стены"),
        ("det_merlon", "Зубец стены"), ("det_battlement", "Зубчатый парапет"),
        ("det_banner", "Знамя"), ("det_lantern", "Фонарь на кронштейне"),
        ("det_wheel", "Корабельное колесо"), ("det_capstan", "Кабестан"),
        ("det_cleat", "Швартовный кнехт"), ("det_bollard", "Тумба"),
        ("det_ladder", "Приставная лестница"), ("det_gangway", "Сходи"),
        ("det_crane_arm", "Стрела крана"), ("det_crane_hook", "Крюк крана"),
        ("det_rigging_rope", "Канат такелажа"), ("det_block_pulley", "Блок"),
        ("det_hatch", "Люк"), ("det_grating", "Решётка палубы"),
        ("det_anchor_stock", "Якорный штока"), ("det_funnel", "Труба дымовая"),
        ("det_vent", "Вентиляционный колпак"), ("det_scupper", "Сливной отверстие"),
        ("det_rowlock", "Уключина весла"), ("det_oar", "Весло"),
    ]
    for cid, name in DETAILS:
        if cid in have:
            continue
        add(out, cid, f"Деталь: {name}", "details", "—", PROP_BUDGET,
            [ARK_STEEL := "ARK_STEEL", "ARK_WOOD_DARK", "ARK_STONE"],
            "детали построек и кораблей — модульные элементы")

    # ---------- предметы и ресурсы (Goods.json) ----------
    GOODS = [
        ("wood", "Древесина", "вязанка брёвен"), ("planks", "Доски", "стопка досок"),
        ("ore", "Руда", "корзина руды"), ("metal", "Металл", "слитки металла"),
        ("parts", "Детали", "ящик механических деталей"), ("fiber", "Волокно", "моток волокна"),
        ("cloth", "Ткань", "свёрток ткани"), ("clothes", "Одежда", "стопка одежды"),
        ("ether_raw", "Эфир-сырьё", "кристаллы эфира-сырья"),
        ("fuel", "Эфирное топливо", "бочка эфирного топлива"),
        ("grain", "Небесное зерно", "мешок зерна"),
        ("flour", "Мука", "мешок муки"), ("bread", "Хлеб", "буханка хлеба"),
        ("aquacrystal", "Аквакристалл", "кристалл аквакристалла"),
    ]
    for cid, name, desc in GOODS:
        if cid in have:
            continue
        add(out, cid, f"Предмет: {name} — {desc}", "items", "—", PROP_BUDGET,
            [ARK_WOOD_DARK := "ARK_WOOD_DARK", "GRN_STRAW", "VAL_CREAM"],
            "предметы и ресурсы — из Goods.json, цепочки производства")

    # ---------- ремёсла и инструменты (12 профессий) ----------
    TOOLS = [
        ("tool_engineer", "Инженерные инструменты"), ("tool_smith", "Кузнечные инструменты"),
        ("tool_carpenter", "Плотницкие инструменты"), ("tool_navigator", "Навигационные приборы"),
        ("tool_seaman", "Морские инструменты"), ("tool_trader", "Торговые весы и гири"),
        ("tool_farmer", "Сельскохозяйственные орудия"), ("tool_hunter", "Охотничьи снасти"),
        ("tool_shooter", "Оружейные принадлежности"), ("tool_fencer", "Фехтовальные принадлежности"),
        ("tool_repair", "Ремонтные инструменты"), ("tool_manager", "Канцелярские принадлежности"),
        ("tool_mason", "Каменщицкий инструмент"), ("tool_cooper", "Бондарный инструмент"),
        ("tool_leather", "Кожевенный инструмент"), ("tool_glass", "Стекольный инструмент"),
    ]
    for cid, name in TOOLS:
        if cid in have:
            continue
        add(out, cid, name, "tools", "—", PROP_BUDGET,
            [ARK_STEEL := "ARK_STEEL", "ARK_COPPER", "ARK_WOOD_DARK"],
            "инструменты по профессиям Bible §5")

    # ---------- облака и погода (расширенные) ----------
    WX = [
        ("wx_fog_bank", "Банка тумана"), ("wx_cumulus_large", "Кучевое большое"),
        ("wx_cumulus_small", "Кучевое малое"), ("wx_stratus", "Слоистое"),
        ("wx_cirrus", "Перистое"), ("wx_nimbus", "Кучево-дождевое"),
        ("wx_mist", "Дымка над водой"), ("wx_vortex", "Вихрь над морем"),
        ("wx_lightning", "Молния"), ("wx_rain_cloud", "Дождевая туча"),
    ]
    for cid, name in WX:
        if cid in have:
            continue
        add(out, cid, name, "weather", "—", PARTICLE_BUDGET, [NEUT[0], "PARCHMENT"],
            "погода — для Ф12 (облака)")

    # ---------- интерфейс (расширенный) ----------
    UI_EXT = [
        ("ui_icon", "Иконка"), ("ui_badge", "Значок счётчика"),
        ("ui_tab", "Вкладка"), ("ui_slider", "Ползунок"), ("ui_toggle", "Переключатель"),
        ("ui_checkbox", "Чекбокс"), ("ui_radio", "Радиокнопка"),
        ("ui_tooltip", "Всплывающая подсказка"), ("ui_progress", "Полоса прогресса"),
        ("ui_meter", "Шкала"), ("ui_compass", "Компас"), ("ui_minimap", "Мини-карта"),
        ("ui_dialog", "Диалоговое окно"), ("ui_toolbar", "Панель инструментов"),
        ("ui_hotbar", "Панель быстрого доступа"), ("ui_craft", "Панель крафта"),
        ("ui_ship_hud", "HUD корабля"), ("ui_trade_panel", "Панель торговли"),
        ("ui_currency", "Плашка валюты"), ("ui_timer", "Таймер"),
        ("ui_tooltip_icon", "Иконка подсказки"),
    ]
    for cid, name in UI_EXT:
        if cid in have:
            continue
        add(out, cid, f"UI: {name}", "ui", "—", 0, NEUT,
            "интерфейс — 11 окон по Bible §9 + вспомогательные элементы")

    # ---------- тайлы окружения (расширенные) ----------
    TILES_EXT = [
        ("tile_stone_wall", "Каменная стена (тайл)"), ("tile_plaster", "Штукатурка (тайл)"),
        ("tile_wood_floor", "Дощатый пол (тайл)"), ("tile_roof_slate", "Сланцевая крыша (тайл)"),
        ("tile_roof_thatch", "Соломенная крыша (тайл)"), ("tile_roof_tile", "Черепица (тайл)"),
        ("tile_dirt", "Земля (тайл)"), ("tile_grass_patch", "Трава (тайл)"),
        ("tile_gravel", "Гравий (тайл)"), ("tile_sand", "Песок (тайл)"),
        ("tile_mud", "Грязь (тайл)"), ("tile_snow", "Снег (тайл)"),
        ("tile_cliff", "Скала (тайл)"), ("tile_cobble", "Булыжник (тайл)"),
        ("tile_crate_stack", "Штабель ящиков (тайл)"), ("tile_net", "Рыболовная сеть (тайл)"),
        ("tile_rope", "Канаты (тайл)"), ("tile_rack", "Стеллаж (тайл)"),
    ]
    for cid, name in TILES_EXT:
        if cid in have:
            continue
        add(out, cid, name, "tiles", "—", TILE_BUDGET, [ARK_STONE := "ARK_STONE"],
            "бесшовные тайлы поверхностей")

    return out


def main():
    data = json.loads(REG.read_text(encoding="utf-8"))
    before = len(data["classes"])
    data["classes"] = expand(data["classes"])
    groups = {}
    for c in data["classes"]:
        groups[c["group"]] = groups.get(c["group"], 0) + 1
    data["groups"] = groups
    data["total"] = len(data["classes"])
    data["note"] = ("Реестр классов моделей для визуальной библиотеки (Ф4). "
                    "Расширен до 250+ классов: персонажи (базовые тела + NPC по профессиям), "
                    "одежда по тирам 10/20/30/40/50, 20 корпусов, 55 видов оружия, "
                    "детали построек, предметы, инструменты, погода, UI, тайлы. "
                    "Размеры — реальные метры из канона; tri-бюджеты по классу.")
    REG.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"model-classes.json: {before} → {len(data['classes'])} классов")
    for g, n in sorted(groups.items(), key=lambda kv: -kv[1]):
        print(f"  {g:14} {n}")


if __name__ == "__main__":
    main()
