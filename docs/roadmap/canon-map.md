# Карта «канон → данные» (Ф1.1)

> Правило: **ни одна игровая цифра не живёт только в тексте.** Каждая строка — это «откуда взяли →
> в какой JSON → в каком поле». Если в каноне два разных значения — фиксируем конфликт, а не выбираем молча.

## Как читать таблицу

- **Источник** — файл и раздел в `docs/` (для `world/*` — файл целиком).
- **Куда** — файл в `GAME_DESIGN/` (или `ROBLOX_IMPLEMENTATION` для тех. лимитов).
- **Статус**: `transfer` — переносим как есть; `test` — число PROPOSED до гейм-теста;
  `conflict` — в доках расхождение, нужно решение (см. `docs/CONTRADICTIONS.md`).

## Фракции и мир

| № | Источник | Что берём | Куда | Статус |
|---|---|---|---|---|
| 1 | `THREE_HORIZONS_PROJECT_BIBLE.md` §2 | 3 фракции: имя, столица, остров, роль, ресурс, форма правления, дом-антагонист | `Factions.json` | transfer |
| 2 | `THREE_HORIZONS_PROJECT_BIBLE.md` §2 | 4 специализации каждой фракции | `Factions.json` → `specializations` | transfer |
| 3 | `THREE_HORIZONS_PROJECT_BIBLE.md` §2 | Эстерхольм и Чёрная Гавань: размеры, высота, население, роль | `Factions.json` → `extrafactional` | transfer |
| 4 | `world/CITY_LAYOUTS.md` | 8 районов каждой столицы | `Factions.json` → `districtsGame` | conflict C-10 |
| 5 | Bible §2 | лорный список районов (крепость/верфь/энергоквартал…) | `Factions.json` → `districtsLore` | conflict C-10 |
| 6 | `DESIGN_TOKENS.md` §«Арквейн/Вальмер/Гринвальд» | 7 токенов палитры на фракцию (HEX + Material) | `Factions.json` → `paletteTokens` | transfer |
| 7 | `world/ISLAND_CATALOG.md` | остров: лор-координаты, размер, роль | `WORLD_COORDINATES` (Ф2) + `Factions.json` → `island` | transfer |
| 8 | `WORLD_MASTER_MAP.md` §«Игровые размеры» | игровые размеры островов и высоты | `constants.json` + `WORLD_COORDINATES.csv` | transfer |
| 9 | `MASTER_SCALE_SPEC.md` §1–§4 | 1 м = 3.571 st (S-01), персонаж, дверь, потолки, лестницы, улицы, причал | `constants.json` | transfer |
| 10 | `WORLD_MASTER_MAP.md` §«Технология» | чанки 100×100 м, стриминг, LOD-импостеры | `constants.json` → `world` | transfer |
| 11 | `world/BUILDING_CATALOG.md` | 7 классов зданий: размер, этажность, функция | `Buildings.json` | transfer |
| 12 | Bible §6 | цепочки производства (5 цепочек) | `Goods.json` → `chains` | transfer |
| 13 | Bible §6 | 3 стратегических лимитных ресурса | `Goods.json` → `strategic` | transfer |
| 14 | `DESIGN_TOKENS.md` §«Стратегические ресурсы» | цвета стратегических ресурсов | `Goods.json` → `token` | transfer |
| 15 | `SPECS_COMBINED.md` §BALANCING | цены корпусов, обслуживание, доход мастерской, шторм, пираты | `Prices.json` | test |
| 16 | `SPECS_COMBINED.md` §BALANCING | прокачка 1–5 ч / 20+ ч | `Professions.json` → `gates` | test |
| 17 | `world/TRADE_ROUTES.md` | 4 маршрута + пиратский рейд | `Routes.json` | transfer |
| 18 | `WORLD_MASTER_MAP.md` §«Маршруты» | расчёт времени при 18 м/с | `travel_times.json` | test |
| 19 | Bible §7 | 4 состояния погоды и их влияние | `Weather.json` | test |
| 20 | `CLOUD_SYSTEM.md` §2.1 | параметры Clouds/Atmosphere по погоде | `Clouds.lua` (конфиг) | transfer |
| 21 | Bible §7 | расписания NPC (3 состояния), агрегация вне видимости | `NPC.json` | transfer |
| 22 | Bible §7 | общие события (одно на всех) + личные квесты | `Quests.json` → `rules` | transfer |
| 23 | Bible §8 | правила поражения: респаун, потеря груза, захват корабля | `Quests.json`/`Prices.json`? → `constants.json` → `defeat` | transfer |

## Корабли и экипаж

| № | Источник | Что берём | Куда | Статус |
|---|---|---|---|---|
| 24 | Bible §4 | 3 корпуса: 18×6, 32×10, 48×15 м; борт 2.5/3.5/4.5 | `Ships.json` → `hulls` | transfer |
| 25 | Bible §4 | 10 категорий модулей и лимиты совместимости | `Ships.json` → `modules` | transfer |
| 26 | Bible §4 | 6 ролей экипажа | `Ships.json` → `crewRoles` | transfer |
| 27 | `MASTER_SCALE_SPEC.md` §4 | studs-габариты корпусов, высота мачты лёгкого | `Ships.json` → `studs` | transfer |
| 28 | `ART_PIPELINE_BLENDER_KIT.md` §тех.правила | триасы, LOD-соотношения, ≤3 материала | `constants.json` → `artBudget` | transfer |

## Профессии, персонажи, экономика

| № | Источник | Что берём | Куда | Статус |
|---|---|---|---|---|
| 29 | Bible §5 | 12 навыков | `Professions.json` → `skills` | transfer |
| 30 | Bible §5 | мультипрофессии разрешены | `Professions.json` → `rules` | transfer |
| 31 | Bible §3 | 3 героя × 2 пола: имя, возраст, фракция, профессия, крючок | `Heroes.json` | transfer |
| 32 | `CONTRADICTIONS.md` C-02 | канон фамилии Морвей / Morwey | `Heroes.json` → `notes` | transfer |
| 33 | `CONTRADICTIONS.md` C-04 | зеркальные возрасты 24 / 26 / 23 | `Heroes.json` | transfer |
| 34 | `CONTRADICTIONS.md` C-03 | боевые специализации Гринвальда (не «фермер») | `Factions.json` + `Professions.json` | transfer |
| 35 | `CONTRADICTIONS.md` C-09 | цепочка волокно→ткань→одежда — APPROVED | `Goods.json` | transfer |

## Технические лимиты (в код, не в GAME_DESIGN)

| № | Источник | Что берём | Куда | Статус |
|---|---|---|---|---|
| 36 | `ARCHITECTURE.md` §5 | near ≤ 8 000 parts, ≤ 60 Remote/с | `constants.json` → `limits` | transfer |
| 37 | `WORLD_NETWORK_ARCHITECTURE.md` §5 | лимиты MessagingService/MemoryStore/DataStore | `constants.json` → `netLimits` | transfer |
| 38 | `SPECS_COMBINED.md` §SECURITY 4 | rate-limit: торговля 5/с, взаимодействие 10/с, чат 3/с | `constants.json` → `rateLimit` | transfer |
| 39 | `ARCHITECTURE.md` §4 | autosave 120 с, ретраи 3×, миграции | `constants.json` → `save` | transfer |
| 40 | `PLATFORM_SUPPORT_SPEC` | TargetRadius 1200/500, тени, LOD−1, кнопки 44pt | `constants.json` → `platform` | transfer |
| 41 | `QUALITY_ASSURANCE.md` | gates A-1/S-1/R-1, бюджет дома ≤60 боксов | `constants.json` → `gates` | transfer |
| 42 | `PROCEDURAL_GENERATION.md` | seed-детерминизм (mulberry32), правила фасада | `constants.json` → `procgen` | transfer |

## UI, звук, облака

| № | Источник | Что берём | Куда | Статус |
|---|---|---|---|---|
| 43 | `UX_DESIGN_SPEC.md` §глаголы | E/F/M/Tab/H и тач-эквиваленты | `constants.json` → `input` | transfer |
| 44 | `UX_DESIGN_SPEC.md` §окна | шаблон «список → детали → действие», 11 окон | `constants.json` → `ui` | transfer |
| 45 | `DESIGN_TOKENS.md` §UI | PARCHMENT/BRASS/INK, радиусы, шрифты | `constants.json` → `uiTokens` | transfer |
| 46 | `AUDIO_DESIGN_BIBLE.md` | темы по зонам, BPM 70–95, правила SFX | `constants.json` → `audio` | transfer |
| 47 | `CLOUD_SYSTEM.md` §2.3 | параметры CloudField: мир 12×12 км, шаг 4 Гц, PUFF_MAX_ACTIVE=6 | `constants.json` → `clouds` | transfer |
| 48 | `CLOUD_SYSTEM.md` §2 + решение S-06 | 3 слоя: нативные Clouds + альфа-клочья + Atmosphere; уровни Y и пухи — Ф12 | `constants.json` → `cloudSea` | transfer |

## Решения и конфликты (в `DECISIONS.md`, не в JSON)

| № | Источник | Что делаем | Куда | Статус |
|---|---|---|---|---|
| 49 | `CONTRADICTIONS.md` C-01 | лор-площади островов = ориентир, игра — из WORLD_MASTER_MAP | `DECISIONS.md` | transfer |
| 50 | `CONTRADICTIONS.md` C-05…C-08 | Эстерхольм/Гавань, дирижабли, сжатие столиц, руины без мистики | `DECISIONS.md` | transfer |
| 51 | S-01…S-06 | масштаб, сжатие, карта, шард, вода, облака | `DECISIONS.md` + `constants.json` | done |
| 52 | Ф1.2 (эта сессия) | **C-10**: районы столиц — Bible §2 vs `CITY_LAYOUTS` | `CONTRADICTIONS.md` | conflict |
| 53 | Ф1.2 (эта сессия) | **C-11**: `ISLAND_CATALOG` «Black Harbor = торговый хаб» vs Bible «Чёрная Гавань = пираты» | `CONTRADICTIONS.md` | conflict |

## Что НЕ переносим в данные

| Источник | Почему |
|---|---|
| `STATUS.md`, `CHANGELOG.md`, `ASSET_REGISTRY.md` | процесс и учёт, а не правила игры |
| — | ~~передача персонажей другому исполнителю~~ — вне зоны v0.1, документы удалены 2026-11-11 |
| `VISUAL_DESIGN_BIBLE.md`, `ART_PIPELINE_BLENDER_KIT.md`, `TEXTURE_PIPELINE.md` | правила арта — в пайплайн, не в JSON |
| `NEW_MAP_LIVING_SEA.md`, `WORLD_SCALE.md` (частично) | эксперименты/устаревшие системы — только как справка по ограничениям |

## Итог

- 53 строки, 13 JSON-файлов `GAME_DESIGN/` + `constants.json`.
- 2 новых конфликта (C-10, C-11) — требуют вашего решения до Ф1.9 и Ф2.
- Ни одна цифра не «придумана»: у каждой есть источник или статус `test`.
