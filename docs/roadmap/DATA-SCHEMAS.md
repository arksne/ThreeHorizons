# СХЕМЫ ДАННЫХ — новые JSON-файлы

> Формат всех игровых данных: `GAME_DESIGN/*.json`, без Roblox-зависимостей (Bible §9).
> Каждая схема ниже — **контракт**: фаза, которая создаёт файл, обязана ему следовать;
> фазы, которые читают, рассчитывают на эти поля.
>
> Правило: **схема меняется только через `docs/DECISIONS.md`** — как и любой другой канон.
> Проверка: `tools/validate_design.py` сверяет файлы с этим документом (после Ф1.13).

## Общие правила

- `schemaVersion: 1` — у всех файлов.
- `generatedFrom: [...]` — список источников в `docs/` (как в уже существующих файлах).
- `status: "APPROVED" | "PROPOSED"` — `PROPOSED` означает «числа не подтверждены тестом».
- Числа — без единиц измерения в имени поля; единица в описании или в ключе (`_M`, `_M2`, `Sec`, `Min`).
- Ни одного `TODO` и ни одного «заглушечного» значения: неизвестное значение — отсутствующее поле, не `0`.

---

## `Style.json` (Ф3.1) — арт-дирекшн и стиль

Источник стиля для всего: палитр, материалов, света, UI.

```jsonc
{
 "schemaVersion": 1,
 "status": "APPROVED",
 "generatedFrom": ["docs/DESIGN_TOKENS.md", "docs/VISUAL_DESIGN_BIBLE.md",
                   "docs/THREE_HORIZONS_PROJECT_BIBLE.md#1"],

 "styleFormula": {
   "formula": "Stylized Realism + Medieval Maritime + Vintage Exploration",
   "axes": [
     {"name": "Stylized Realism", "means": "реалистичные пропорции, упрощённая форма"},
     {"name": "Medieval Maritime", "means": "средневековая морская техника и корабли"},
     {"name": "Vintage Exploration", "means": "винтажная палитра, типографика, ретушь"}
   ],
   "antiExamples": ["фэнтези", "стимпанк", "мультяшно", "гиперреализм"]
 },

 "artPriority": "text",              // "text" — приоритет текста над атласом (D-001)
 "knownArtDeviations": [              // признанные ошибки генерации артов
   {"topic": "фамилия Морвей", "note": "«Моряк» — ошибка, канон «Морвей / Morwey»"},
   {"topic": "специализация «фермер»", "note": "это профессия, не боевая специализация"},
   {"topic": "«древние руины»", "note": "заброшенные поселения, без мистики (C-08)"},
   {"topic": "площадь Гавани", "note": "0.8×0.6 км, а не 0.48 (C-05)"}
 ],

 "factionTokens": {                   // 21 токен: 7 × 3 фракции
   "arkvein": [
     {"id": "ARK_GRAPHITE", "hex": "#2B2E33", "usage": "крыши, металл тёмный",
      "material": "Slate"}
   ]
 },

 "uiTokens": [                       // 7 общих токенов
   {"id": "INK", "hex": "#1E1A14", "usage": "обводка UI, текст тёмный"}
 ],

 "materials": [                       // токен → материал Roblox
   {"token": "ARK_GRAPHITE", "material": "Slate"}
 ],

 "lighting": {
   "factions": {
     "arkvein": {"colorTempK": 6500, "exposure": -0.2, "fog": "light"},
     "valmer":  {"colorTempK": 5600, "exposure": 0,    "fog": "none"},
     "grinwald":{"colorTempK": 5200, "exposure": 0,    "saturation": 0.1}
   },
   "common": {"atmosphereDensity": 0.35, "haze": 2, "cloudsCover": 0.6},
   "storm":  {"atmosphereDensity": 0.7}
 },

 "gateA1": [                          // 8 пунктов худконтроля
   {"id": "hexFromTokens", "title": "HEX из токенов", "check": "hex в Style.json"},
   {"id": "scaleSpec", "title": "масштаб по MASTER_SCALE_SPEC", "check": "габарит в м"},
   {"id": "nameTH", "title": "имя TH_*", "check": "regex ^TH_[A-Z]{3}_"},
   {"id": "status", "title": "статус concept|blockout|final|lod", "check": "поле status"},
   {"id": "materialsMax3", "title": "материалов ≤ 3", "check": "count ≤ 3"},
   {"id": "hasUV", "title": "UV есть", "check": "uv layer"},
   {"id": "lodRatio", "title": "LOD 35 % / 8 %", "check": "tri vs L0"},
   {"id": "pivotBase", "title": "пивот в основании", "check": "y = 0"}
 ]
}
```

**Читают:** Ф4 (рендеры — палитра и свет), Ф6 (текстуры — палитра), Ф7 (ассеты — токены и материалы),
Ф9 (мир — свет столицы), Ф14 (UI — 7 токенов), Ф16 (механики — стратегические ресурсы по цвету).

---

## `Combat.json` (Ф13.1) — бой, абордаж, захват

```jsonc
{
 "schemaVersion": 1,
 "status": "PROPOSED",                // числа баланса — до гейм-теста
 "generatedFrom": ["docs/THREE_HORIZONS_PROJECT_BIBLE.md#4",
                   "docs/THREE_HORIZONS_PROJECT_BIBLE.md#8"],

 "hulls": [
   {"id": "light",  "guns": 2, "gunDamage": 12, "reloadSec": 2.5, "hullHp": 300},
   {"id": "medium", "guns": 4, "gunDamage": 18, "reloadSec": 3.0, "hullHp": 500},
   {"id": "heavy",  "guns": 6, "gunDamage": 26, "reloadSec": 3.5, "hullHp": 800}
 ],
 "ammo": {"itemId": "ammo_ball", "pricePerShot": 1, "maxCarry": 120},
 "boarding": {"rangeM": 12, "transferSec": 8, "vulnerabilityMult": 1.5},
 "capture": {"flagItemId": "enemy_flag", "transferCargo": true, "respawnShieldSec": 5},
 "losses": {"cargoLossShare": 0.4, "skillLoss": false, "safePointEnabled": true}
}
```

**Читают:** Ф13 (бой), Ф16 (потеря груза, экономика), Ф18 (NPC-флот — наследует боевые параметры).

---

## `Interiors.json` (Ф11.1–11.2) — помещения

```jsonc
{
 "schemaVersion": 1,
 "status": "APPROVED",
 "generatedFrom": ["docs/THREE_HORIZONS_PROJECT_BIBLE.md#4",
                   "docs/world/BUILDING_CATALOG.md",
                   "docs/MASTER_SCALE_SPEC.md#2"],

 "shipRooms": [
   {"id": "bridge", "name": "Рубка", "areaM2": 12, "heightM": 2.7,
    "gridM": 1, "walls": [{"x":0,"z":0,"w":6,"d":4}],
    "openings": [{"wall": 0, "atM": 2.0, "type": "door", "wM": 1.0, "hM": 2.1}],
    "furniture": [{"id": "wheel", "x": 3, "z": 2, "rotDeg": 0}],
    "interactions": [{"id": "helm", "label": "Штурвал", "action": "control_ship"}],
    "lights": [{"x": 3, "z": 2, "brightness": 1.5}]
   }
 ],
 "buildingRooms": [
   {"id": "house_generic", "forClass": "house_small", "areaM2": 18, "heightM": 2.7,
    "gridM": 1, "walls": [], "openings": [], "furniture": [],
    "interactions": [{"id": "rest", "label": "Отдых", "action": "rest"}]}
 ],
 "furnitureCatalog": [
   {"id": "table", "wM": 1.2, "dM": 0.75, "hM": 0.75}
 ]
}
```

**Читают:** Ф11 (генератор), Ф9 (рубка корабля), Ф16 (механики — `action` из интеракций),
Ф13 (каюта капитана — место захвата), Ф21 (торговая контора).

**Правило:** `action` интеракции обязан существовать в механиках Ф16 — иначе интерьер пустой.

---

## `Fleet.json` (Ф18.1) — NPC-флот

```jsonc
{
 "schemaVersion": 1,
 "status": "PROPOSED",
 "generatedFrom": ["docs/THREE_HORIZONS_PROJECT_BIBLE.md#4",
                   "docs/THREE_HORIZONS_PROJECT_BIBLE.md#7"],

 "tickSec": 300,                    // офлайн-тик (5 мин)
 "capHours": 24,                    // после этого корабль «засыпает»
 "routes": [
   {"id": "arkvein_hub", "ships": [
     {"id": "npc_ark_1", "hullId": "medium", "speedMs": 18,
      "cycleSec": 3600, "cargoItemIds": ["metal_parts"], "count": 40}
   ]}
 ],
 "events": [
   {"id": "pirate_attack", "radiusM": 500, "shared": true,
    "reactions": ["help", "avoid"], "rewardItemId": null}
 ]
}
```

**Читают:** Ф18 (симуляция), Ф16 (продажа NPC-товара), Ф19 (событие в сюжете).

**Правило:** `shared: true` → событие одно на всех в радиусе (Bible §7), копий по числу игроков нет.

---

## `Settlements.json` (Ф20.1) — малые поселения и POI

```jsonc
{
 "schemaVersion": 1,
 "status": "APPROVED",
 "generatedFrom": ["docs/THREE_HORIZONS_PROJECT_BIBLE.md#1",
                   "docs/THREE_HORIZONS_PROJECT_BIBLE.md#2",
                   "docs/WORLD_MASTER_MAP.md"],

 "settlements": [
   {"id": "bronze_hill", "name": "Бронзовый Холм", "island": "arkvein",
    "gameXM": 3000, "gameZM": 2000, "sizeM": [60, 40],
    "kind": "farm", "npcId": "npc_bronze", "recipeId": "planks",
    "minIslandDistStuds": 600, "minRouteDistStuds": 300}
 ],
 "poi": [
   {"id": "wreck_01", "kind": "wreck", "gameXM": 5200, "gameZM": 8000,
    "lootItemId": "scrap", "lootCount": 3}
 ],
 "miniIslands": [
   {"id": "A1", "name": "Рыболовный форпост", "gameXM": 3000, "gameZM": 2000,
    "sizeM": [42, 30], "role": "Промысловый: рыба", "structureId": "hut"}
 ]
}
```

**Читают:** Ф20 (размещение), Ф9 (мир — постройки), Ф16 (NPC и рецепты), Ф2 (карта — координаты).

**Правило:** расстояния проверяются `tools/validate_world.py` — это критерий шага 20.2.

---

## `Strings.json` (Ф17.1) — локализация

```jsonc
{
 "schemaVersion": 1,
 "status": "APPROVED",
 "generatedFrom": ["docs/THREE_HORIZONS_PROJECT_BIBLE.md#9",
                   "docs/UX_DESIGN_SPEC.md"],

 "entries": [
   {"key": "ui.window.inventory.title", "ru": "Склад", "en": "Warehouse",
    "category": "ui", "maxLen": 24}
 ],
 "categories": ["ui", "quest", "item", "hint", "error", "system", "chat", "tutorial"]
}
```

**Читают:** Ф17 (локализация), Ф14 (UI), Ф16 (квесты и товары), Ф19 (реплики NPC), Ф13 (сообщения боя).

**Правило:** ключ `<категория>.<контекст>.<смысл>`; `maxLen` — предел вёрстки, не украшение.

---

## `World.json` (Ф2.2) — геометрия мира

Создаётся генератором `tools/world_geometry.py` из `constants.json` — **не редактируется руками**.

```jsonc
{
 "schemaVersion": 1,
 "status": "APPROVED",
 "generatedFrom": ["docs/WORLD_MASTER_MAP.md", "docs/world/ISLAND_CATALOG.md",
                   "docs/DECISIONS.md#S-07"],

 "frame": "S-07",
 "mapGameM": [18000, 26000],
 "mapStuds": [64278, 92846],
 "seaY": 0,
 "islands": [
   {"id": "arkvein", "name": "Арквейн", "faction": "arkvein",
    "loreXM": 90000, "loreZM": 40000, "loreWM": 12000, "loreDM": 9000,
    "gameXM": 9000, "gameZM": 4000, "gameWM": 1200, "gameDM": 900,
    "studsX": 32139, "studsZ": 14284, "studsW": 4285, "studsD": 3214,
    "heightM": 280,
    "heights": {"seaY": 0, "lowY": 300, "plateauY": 550, "peakY": 1000},
    "capital": "arkenhold", "capitalSizeM": [250, 200]}
 ],
 "miniIslands": [],
 "travelTimes": [
   {"id": "arkvein_hub", "from": "arkvein", "to": "black_harbor",
    "distanceGameM": 9605, "distanceStuds": 34300, "distanceLoreKm": 96.1,
    "seconds": 534, "minutes": 8.9, "speedMs": 18}
 ]
}
```

**Читают:** Ф9 (квартал), Ф10 (маршруты кораблей), Ф12 (погода), Ф14 (карта в UI), Ф20 (поселения),
Ф22 (проверка целостности).

**Правило:** генерируется из `constants.json`; правка вручную = баг.

---

## `arkenhold_blocks.json` (Ф2.8) — сетка кварталов столицы

```jsonc
{
 "schemaVersion": 1,
 "status": "APPROVED",
 "generatedFrom": ["docs/world/CITY_LAYOUTS.md", "GAME_DESIGN/Buildings.json",
                   "docs/MASTER_SCALE_SPEC.md#3", "docs/DECISIONS.md#S-09"],

 "city": "arkenhold",
 "citySizeM": [250, 200],
 "grid": {"cols": 4, "rows": 2,
          "streetMainM": 8, "streetSecondaryM": 4, "buildingGapM": 3},
 "waterSide": "east",

 "blocks": [
   {"id": "central_square", "name": "Центральная площадь",
    "x": 0, "z": 0, "w": 57.5, "d": 96,
    "waterfront": false, "streetSide": "south",
    "buildingKinds": ["tavern", "house_medium", "house_medium"],
    "buildings": [
      {"kind": "tavern", "x": 0, "z": 72, "w": 18, "d": 24,
       "rotationDeg": 0, "facade": "south"}
    ]}
 ],
 "streets": [
   {"id": "street_v0", "kind": "main", "x": 57.5, "z": 0,
    "w": 8, "d": 200, "orientation": "vertical"}
 ],
 "totals": {"blockAreaM2": 44160, "streetAreaM2": 6000,
            "cityAreaM2": 50000, "blockShare": 0.8832}
}
```

**Читают:** Ф9 (квартал собирается в мир), Ф6 (ассеты ставятся по `buildingKinds`), Ф22 (проверка).

**Правила:**
- `blocks` + `streets` **покрывают город без остатка** — проверяется `tools/validate_world.py`.
- Здание стоит **вдоль улицы** (`facade` = `streetSide`), зазор между зданиями ≥ `buildingGapM` (3 м).
- `x`,`z` — координаты **внутри квартала** (не города).

---

## Что ещё появится

| Файл | Фаза | Назначение |
|---|---|---|
| `GAME_DESIGN/visual_library.json` | Ф4.1 | реестр 52 классов моделей (id, группа, габарит, tri-бюджет, материалы) |
| `docs/story/PLOT.md` | Ф19.1 | акты, узлы, кто что знает, 3 улики, 2 финала |
| `ROADMAP_0.2.md` | Ф13.9 | backlog после закрытия боевой фазы |
| `blender/manifest.json` | Ф5.7 | реестр экспортированных ассетов |
| `blender/textures/manifest.json` | Ф6.1 | реестр 69 текстур с HEX и тайлингом |
