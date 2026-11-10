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
| Ресурс | HEX | Material | Применение |
|---|---|---|---|
| ETHER_FUEL | #3FA7FF | Neon | эфирное топливо, свечение баков |
| AQUACRYSTAL | #7FD4FF | Glass | аквакристалл, резервуары Вальмера |
| SKY_GRAIN | #D8A93B | — | небесное зерно, амбары Гринвальда |

> Материал SKY_GRAIN не зафиксирован: зерно красится через SurfaceAppearance (Ф6). Остальные два — сток Roblox.

## Облачное море и небо (APPROVED)
| Токен | HEX | Применение |
|---|---|---|
| CLOUD_LIGHT | #EDE6D3 | облака в свету (верхние плоскости, подсвет) |
| CLOUD_SILVER | #C9C2B4 | облака в серебре (средний тон) |
| CLOUD_SHADOW | #A9A396 | облака в тени (нижние плоскости) |
| CLOUD_HAZE | #CBB98F | дальняя дымка, горизонт |
| SKY_PALE | #B8BEB4 | бледное небо с лёгкой сепиёй |

## Свет и атмосфера (APPROVED)
| Остров | ColorTemp | Экспозиция | Насыщенность | Туман | Вода |
|---|---|---|---|---|---|
| Арквейн | 6500K | −0.2 | 0 | лёгкий | — |
| Вальмер | 5600K | 0 | 0 | нет | Reflectance 0.4 |
| Гринвальд | 5200K | 0 | +0.1 | — | — |

| Общее | Значение |
|---|---|
| Atmosphere Density | 0.35 |
| Haze | 2 |
| Clouds Cover | 0.6 |
| Шторм Atmosphere Density | 0.7 |
| Ветер на дрейф кораблей | множитель в GAME_DESIGN |
| Шрифт заголовков UI | serif с засечками (Antique, fallback serif) |
| Шрифт тела UI | sans 14–16 px |
| Радиус скругления | 4 px |
| Рамка | 2 px BRASS |

## Правило худконтроля
Новый ассет обязан ссылаться на токены выше; «примерно похожий цвет» запрещён. Проверка — gate A-1.
