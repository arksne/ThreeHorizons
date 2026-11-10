# STYLE BIBLE — арт-дирекшн и стиль

> Сгенерировано из `GAME_DESIGN/Style.json` (`tools/build_style.py`).
> Правки — в `docs/DESIGN_TOKENS.md`: он и есть источник HEX.

## Стиль

**Stylized Realism + Medieval Maritime + Vintage Exploration**

- **Stylized Realism** — реалистичные пропорции, упрощённая форма
- **Medieval Maritime** — средневековая морская техника и корабли
- **Vintage Exploration** — винтажная палитра, типографика, ретушь

Не делаем: фэнтези, стимпанк, мультяшно, гиперреализм

## Приоритет

**D-001: при конфликте атласа с Master Prompt побеждает текст. Атлас — референс формы и палитры, не правил.**

Признанные расхождения арта:

- фамилия Морвей — «Моряк» — ошибка, канон «Морвей / Morwey» (C-02)
- специализация «фермер» — это профессия, не боевая специализация (C-03)
- «древние руины» — заброшенные поселения, без мистики (C-08)
- площадь Гавани — 0.8×0.6 км, а не 0.48 (C-05)

## Палитры фракций

### arkvein

| Токен | HEX | Применение | Материал |
|---|---|---|---|
| `ARK_GRAPHITE` | #2B2E33 | крыши, металл тёмный | Slate, Metal |
| `ARK_STONE` | #5A5C60 | стены, камень | Cobblestone |
| `ARK_WOOD_DARK` | #4A3226 | балки, двери | WoodPlanks |
| `ARK_BURGUNDY` | #6E2A2A | акценты, флаги | Fabric |
| `ARK_COPPER` | #8C5A3B | механизмы, трубы | Metal |
| `ARK_STEEL` | #9AA2A8 | оковки, механизмы | DiamondPlate |
| `ARK_PLASTER` | #C9C2B4 | вставки стен | Plaster |

### valmer

| Токен | HEX | Применение | Материал |
|---|---|---|---|
| `VAL_LIMESTONE` | #EDE6D3 | фасады | Limestone |
| `VAL_CREAM` | #D9C9A8 | декор, арки | Plaster |
| `VAL_SAND` | #B99B6B | цоколи, мостовые | Sandstone |
| `VAL_TEAL` | #4E7E8C | ставни, ткань | Fabric |
| `VAL_SEA` | #2E4E7E | крыши, флаги | Slate |
| `VAL_BRONZE` | #A87F3F | купола, светильники | Metal |
| `VAL_WHITE` | #F5F1E6 | камень белый | Marble |

### grinwald

| Токен | HEX | Применение | Материал |
|---|---|---|---|
| `GRN_OLIVE` | #5A6B3C | ставни, ткань | Fabric |
| `GRN_FOREST` | #3E5230 | крыши тёмные | Wood |
| `GRN_WOOD` | #6B4A2E | каркас, балки | WoodPlanks |
| `GRN_BEIGE` | #D8C9A3 | штукатурка | Plaster |
| `GRN_STRAW` | #C2A35C | крыши солома/черепица светлая | Wood |
| `GRN_TERRA` | #A55A35 | черепица, кирпич | Brick |
| `GRN_STONE` | #8A8578 | камень | Cobblestone |

## Общие токены UI

| Токен | HEX | Применение |
|---|---|---|
| `INK` | #1E1A14 | обводка UI, текст тёмный |
| `PARCHMENT` | #E8DCC0 | фон UI, пергамент |
| `PARCH_DARK` | #CBB98F | фон UI вторичный |
| `BRASS` | #B08D3E | рамки, латунь UI |
| `WOOD_UI` | #3A2A1C | панели тёмного дерева |
| `DANGER` | #8C2B1B | урон/пираты |
| `FOCUS_BLUE` | #2E4E7E | акцент Вальмера/воды |

## Стратегические ресурсы

| Ресурс | HEX | Material | Применение |
|---|---|---|---|
| `ETHER_FUEL` | #3FA7FF | Neon | эфирное топливо, свечение баков |
| `AQUACRYSTAL` | #7FD4FF | Glass | аквакристалл, резервуары Вальмера |
| `SKY_GRAIN` | #D8A93B | SurfaceAppearance (Ф6) | небесное зерно, амбары Гринвальда |

## Свет и атмосфера

| Остров | ColorTemp | Экспозиция | Насыщенность | Туман | Вода |
|---|---|---|---|---|---|
| arkvein | 6500K | -0.2 | 0 | лёгкий | — |
| valmer | 5600K | 0 | 0 | нет | 0.4 |
| grinwald | 5200K | 0 | 0.1 | — | — |

| Общее | Значение |
|---|---|
| atmosphereDensity | 0.35 |
| haze | 2.0 |
| cloudsCover | 0.6 |
| stormAtmosphereDensity | 0.7 |
| windDriftNote | множитель в GAME_DESIGN |

## Шрифты UI

- **title**: serif с засечками (Antique, fallback serif)
- **body**: sans 14–16 px
- **radiusPx**: 4
- **border**: 2 px BRASS

## Gate A-1 — чек-лист худконтроля

| # | Пункт | Проверка |
|---|---|---|
| 1 | HEX из токенов | все цвета ассета есть в factionTokens/uiTokens/strategicResources |
| 2 | масштаб по MASTER_SCALE_SPEC | габарит совпадает с заявленным в classes/dimsM |
| 3 | имя TH_* | имя начинается с TH_ и в верхнем регистре |
| 4 | статус concept|blockout|final|lod | поле status из допустимых |
| 5 | материалов ≤ 3 | len(materials) ≤ 3 |
| 6 | UV есть | uvLayers > 0 |
| 7 | LOD 35 % / 8 % | triL1 ≈ 35 % ±3 % triL0, triL2 ≈ 8 % ±2 % triL0 |
| 8 | пивот в основании | origin = base_center, низ модели на y = 0 |

Проверка: `python -X utf8 tools/validate_style.py <манифест ассета>` → вердикт по каждому пункту.
