# DESIGN TOKENS (APPROVED v0.1)
> Источник палитр: 9 атласов (ref01–ref09). HEX сняты как канон-токены; материалы — Roblox Material + SurfaceAppearance.

## Арквейн — строгий, индустриальный (APPROVED)
| Токен | HEX | Применение | Material |
|---|---|---|---|
| ARK_GRAPHITE | #2B2E33 | крыши, металл тёмный | Slate / Metal |
| ARK_STONE | #5A5C60 | стены, камень | Cobblestone |
| ARK_WOOD_DARK | #4A3226 | балки, двери | WoodPlanks |
| ARK_BURGUNDY | #6E2A2A | акценты, флаги | Fabric |
| ARK_COPPER | #8C5A3B | механизмы, трубы | Metal |
| ARK_STEEL | #9AA2A8 | оковки, механизмы | DiamondPlate |
| ARK_PLASTER | #C9C2B4 | вставки стен | Plaster |

## Вальмер — светлый, торговый (APPROVED)
| Токен | HEX | Применение | Material |
|---|---|---|---|
| VAL_LIMESTONE | #EDE6D3 | фасады | Limestone |
| VAL_CREAM | #D9C9A8 | декор, арки | Plaster |
| VAL_SAND | #B99B6B | цоколи, мостовые | Sandstone |
| VAL_TEAL | #4E7E8C | ставни, ткань | Fabric |
| VAL_SEA | #2E4E7E | крыши, флаги | Slate |
| VAL_BRONZE | #A87F3F | купола, светильники | Metal |
| VAL_WHITE | #F5F1E6 | камень белый | Marble |

## Гринвальд — природный (APPROVED)
| Токен | HEX | Применение | Material |
|---|---|---|---|
| GRN_OLIVE | #5A6B3C | ставни, ткань | Fabric |
| GRN_FOREST | #3E5230 | крыши тёмные | Wood |
| GRN_WOOD | #6B4A2E | каркас, балки | WoodPlanks |
| GRN_BEIGE | #D8C9A3 | штукатурка | Plaster |
| GRN_STRAW | #C2A35C | крыши солома/черепица светлая | Wood |
| GRN_TERRA | #A55A35 | черепица, кирпич | Brick |
| GRN_STONE | #8A8578 | камень | Cobblestone |

## Общие (APPROVED)
| Токен | HEX | Применение |
|---|---|---|
| INK | #1E1A14 | обводка UI, текст тёмный |
| PARCHMENT | #E8DCC0 | фон UI, пергамент |
| PARCH_DARK | #CBB98F | фон UI вторичный |
| BRASS | #B08D3E | рамки, латунь UI |
| WOOD_UI | #3A2A1C | панели тёмного дерева |
| DANGER | #8C2B1B | урон/пираты |
| FOCUS_BLUE | #2E4E7E | акцент Вальмера/воды |

## Стратегические ресурсы — цветовой код (APPROVED)
Эфирное топливо — светящийся синий #3FA7FF (Neon); аквакристалл — ледяной #7FD4FF (Glass); небесное зерно — золото #D8A93B.

## Свет и атмосфера (APPROVED)
- Арквейн: ColorTemp 6500K, туман лёгкий, экспозиция −0.2. Вальмер: 5600K, яркий день, вода Reflectance 0.4. Гринвальд: 5200K тёплый, насыщенность +0.1.
- Общие: Atmosphere Density 0.35, Haze 2, Clouds Cover 0.6; шторм — Density 0.7, Wind влияет на дрейф кораблей (множитель в GAME_DESIGN).
- Шрифты UI: заголовки — serif с засечками (Antique/serif fallback), тело — читаемый sans 14–16px; радиусы 4px, рамки 2px BRASS.

## Правило худконтроля
Новый ассет обязан ссылаться на токены выше; «примерно похожий цвет» запрещён. Проверка — gate A-1.
