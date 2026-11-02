# ASSET REGISTRY (v1.1 — полный проект + текстурный пак, живёт и пополняется, дублей не создавать)
> Формат: AssetID | Название | Категория | Версия | Источник | Размер (м) | Материалы/токены | LOD | Статус | Использование.
> Статус: concept | blockout | final | lod. Gate A-1 обязателен для final.

## Архитектура — Арквейн (первые слоты под генератор)
| ID | Название | Кат. | Вер. | Источник | Размер | Материалы | LOD | Статус | Использование |
|---|---|---|---|---|---|---|---|---|---|
| TH_ARK_House_01 | Дом горожанина | arch | 0.1 | BuildingGenerator(ark) | 8×7×9(h) | ARK_STONE/ARK_WOOD_DARK/ARK_GRAPHITE | L0 | blockout | Аркенхольд, жилые |
| TH_ARK_Tower_01 | Часовая башня | arch | 0.1 | BuildingGenerator(ark,tower) | 6×6×18 | ARK_STONE/ARK_COPPER | L0 | blockout | Площади |
| TH_ARK_Workshop_01 | Мастерская | arch | 0.1 | BuildingGenerator(ark,workshop) | 12×8×7 | ARK_STONE/ARK_STEEL | L0 | blockout | Промзона |
| TH_ARK_Roof_Kit | Набор крыш (3 типа) | arch/kit | 0.1 | ArchitectureGenerator | — | ARK_GRAPHITE | L0 | blockout | Все дома |
| TH_ARK_DoorWin_Kit | Двери/окна 1.0×2.1 | arch/kit | 0.2 | ArchitectureGenerator.doorKit/windowKit + blender/ark_kits.py | 1.0×2.1 / 0.9×1.2 | ARK_WOOD_DARK/Glass | L0 | blockout | Все дома |
| TH_ARK_Bridge_01 | Мост с фонарями | arch/kit | 0.2 | ArchitectureGenerator.bridge | секция 12×3 | ARK_WOOD_DARK/ARK_COPPER | L0 | blockout | Каналы Вальмары (адаптация) |
| TH_ARK_Arch_01 | Арка 3м | arch/kit | 0.2 | ArchitectureGenerator.arch | 3×3 | ARK_STONE | L0 | blockout | Площади, ворота |
| TH_SHIP_Light_18 | Лёгкий корпус 18м | ship | 0.2 | ShipGenerator(light) | 18×6 | SHIP_HULL/парус фракции | L0 | blockout | Разведка |
| TH_SHIP_Med_32 | Средний корпус 32м | ship | 0.2 | ShipGenerator(medium) | 32×10 | SHIP_HULL/парус фракции | L0 | blockout | Универсал |
| TH_SHIP_Heavy_48 | Тяжёлый корпус 48м | ship | 0.2 | ShipGenerator(heavy) | 48×15 | SHIP_HULL/парус фракции | L0 | blockout | Груз/бой |
| TH_INT_TableSet_01 | Стол+стул | interior | 0.2 | InteriorGenerator.tableSet | 1.6×1.0 h0.75 | INT_WOOD | L0 | blockout | Каюты, таверны |
| TH_INT_Bed_01 | Кровать 2.0×0.9 | interior | 0.2 | InteriorGenerator.bed | 2.0×0.9 | INT_WOOD/INT_CLOTH | L0 | blockout | Каюты, дома |
| TH_INT_Workbench_ARK | Верстак | interior | 0.2 | InteriorGenerator.workbench | 2.0×0.8 | INT_WOOD/ARK_COPPER | L0 | blockout | Мастерские |
| TH_ENV_IsleChunk_100 | Чанк острова 100м | env | 0.2 | EnvironmentGenerator.islandChunk | 100×100 | почва фракции/ROCK | L0 | blockout | Все острова |
| TH_ENV_Tree_01 | Дерево 4–7м | env | 0.2 | EnvironmentGenerator.tree | h4–7 | GRN_WOOD/GRN_FOREST | L0 | blockout | Гринвальд, парки |
| TH_DECO_Barrel_01 | Бочка d0.6 h0.9 | deco | 0.2 | DecorationGenerator.barrel | d0.6 h0.9 | INT_WOOD/ARK_STEEL | L0 | blockout | Порты, трюмы |
| TH_DECO_Lamp_01 | Фонарь h2.8 | deco | 0.2 | DecorationGenerator.lampPost | h2.8 | ARK_COPPER/LAMP | L0 | blockout | Улицы, мосты |
| TH_DECO_Stall_01 | Рыночный прилавок | deco | 0.2 | DecorationGenerator.marketStall | 2.0×1.0 | INT_WOOD/ткань фракции | L0 | blockout | Рынки |
| TH_DIST_Arkenhold_Q1 | Квартал Аркенхольда (блок-аут) | district | 0.2 | DistrictLayout 3×3 | ~150×150м | — | L0 | blockout | Аркенхольд-центр |
| TH_VAL_House_01 | Дом Вальмера светлый | arch | 0.3 | BuildingGenerator(valmere) + blender/val_green_houses.py | 8×7×2эт | VAL_LIMESTONE/VAL_SEA/VAL_BRONZE | L0 | blockout | Вальмара, жилые |
| TH_GRN_Farm_01 | Ферма Гринвальда | arch | 0.3 | BuildingGenerator(greenwald) + blender/val_green_houses.py | 10×8 | GRN_BEIGE/GRN_TERRA/GRN_WOOD | L0 | blockout | Гринхольм, фермы |
| TH_VAL_Aqueduct_01 | Акведук секция | arch/kit | 0.3 | ArchitectureGenerator.aqueduct + blender | секция 24м h8 | VAL_LIMESTONE | L0 | blockout | Вальмара, водный квартал |
| TH_GRN_Mill_01 | Мельница | arch | 0.3 | ArchitectureGenerator.windmill + blender | h12+ | GRN_BEIGE/GRN_TERRA | L0 | blockout | Гринвальд, поля |
| TH_SHIP_Med_32_FBX | Средний корпус FBX | ship/fbx | 0.3 | blender/ships.py --hull medium | 32×10 | SHIP_HULL/SHIP_SAIL | L0 | blockout | Верфи |
| TH_ENV_Tree_01 | Дерево 4–7м | env | 0.2 | EnvironmentGenerator.tree | h4–7 | GRN_WOOD/GRN_FOREST | L0 | blockout | Гринвальд, парки |

## Единый каталог деталей (APPROVED — размеры канона, переиспользовать везде)
- Дверь: 1.0×2.1 м. Окно: 0.9×1.2, подоконник 0.9 м. Лестничный марш: 0.25/0.18. Балка: 0.2×0.2. Доска: 0.03×0.25. Бочка: d0.6 h0.9. Ящик: 0.6³. Фонарь: h2.8. Причальная тумба: 0.5×0.5×0.9.
- Материалы по фракциям — только DESIGN_TOKENS.

## POI / окружение (слоты)
TH_SKY_IslandBase (Terrain-шаблон), TH_SKY_CloudBank, TH_SKY_Wreck (обломки), TH_SKY_Dock_Med (40×14 м).

## Корабли (слоты)
TH_SHIP_Light_18 / TH_SHIP_Med_32 / TH_SHIP_Heavy_48 — корпуса; модули TH_SHIP_Engine_*, TH_SHIP_Sail_*.

## Запрет дублей
Перед новым ассетом — grep по этому файлу. Совпадение размера ±10% и материала — переиспользовать.

## Текстуры (v1.1, процедурные)
| ID | Название | Кат. | Вер. | Источник | Размер | HEX | LOD | Статус | Файлы |
|---|---|---|---|---|---|---|---|---|---|
| TH_TEX_ARK_Stone | Текстура ARK_Stone (stone) | texture | 1.1 | tools/gen_textures.py | 512×512 | #5A5C60 | — | final (ждёт upload) | TH_TEX_ARK_Stone_a.png + _n/_r |
| TH_TEX_ARK_Cobble | Текстура ARK_Cobble (cobble) | texture | 1.1 | tools/gen_textures.py | 512×512 | #57585C | — | final (ждёт upload) | TH_TEX_ARK_Cobble_a.png + _n/_r |
| TH_TEX_ARK_WoodDark | Текстура ARK_WoodDark (planks) | texture | 1.1 | tools/gen_textures.py | 512×512 | #4A3226 | — | final (ждёт upload) | TH_TEX_ARK_WoodDark_a.png + _n/_r |
| TH_TEX_ARK_Slate | Текстура ARK_Slate (slate) | texture | 1.1 | tools/gen_textures.py | 512×512 | #2B2E33 | — | final (ждёт upload) | TH_TEX_ARK_Slate_a.png + _n/_r |
| TH_TEX_ARK_Copper | Текстура ARK_Copper (copper) | texture | 1.1 | tools/gen_textures.py | 512×512 | #8C5A3B | — | final (ждёт upload) | TH_TEX_ARK_Copper_a.png + _n/_r |
| TH_TEX_ARK_Steel | Текстура ARK_Steel (metal) | texture | 1.1 | tools/gen_textures.py | 512×512 | #9AA2A8 | — | final (ждёт upload) | TH_TEX_ARK_Steel_a.png + _n/_r |
| TH_TEX_VAL_Limestone | Текстура VAL_Limestone (limestone) | texture | 1.1 | tools/gen_textures.py | 512×512 | #EDE6D3 | — | final (ждёт upload) | TH_TEX_VAL_Limestone_a.png + _n/_r |
| TH_TEX_VAL_Cream | Текстура VAL_Cream (plaster) | texture | 1.1 | tools/gen_textures.py | 512×512 | #D9C9A8 | — | final (ждёт upload) | TH_TEX_VAL_Cream_a.png + _n/_r |
| TH_TEX_VAL_Sand | Текстура VAL_Sand (stone) | texture | 1.1 | tools/gen_textures.py | 512×512 | #B99B6B | — | final (ждёт upload) | TH_TEX_VAL_Sand_a.png + _n/_r |
| TH_TEX_VAL_SeaSlate | Текстура VAL_SeaSlate (slate) | texture | 1.1 | tools/gen_textures.py | 512×512 | #2E4E7E | — | final (ждёт upload) | TH_TEX_VAL_SeaSlate_a.png + _n/_r |
| TH_TEX_VAL_Bronze | Текстура VAL_Bronze (metal) | texture | 1.1 | tools/gen_textures.py | 512×512 | #A87F3F | — | final (ждёт upload) | TH_TEX_VAL_Bronze_a.png + _n/_r |
| TH_TEX_VAL_WhiteMarble | Текстура VAL_WhiteMarble (marble) | texture | 1.1 | tools/gen_textures.py | 512×512 | #F5F1E6 | — | final (ждёт upload) | TH_TEX_VAL_WhiteMarble_a.png + _n/_r |
| TH_TEX_VAL_TealCanvas | Текстура VAL_TealCanvas (canvas) | texture | 1.1 | tools/gen_textures.py | 512×512 | #4E7E8C | — | final (ждёт upload) | TH_TEX_VAL_TealCanvas_a.png + _n/_r |
| TH_TEX_GRN_Plaster | Текстура GRN_Plaster (plaster) | texture | 1.1 | tools/gen_textures.py | 512×512 | #D8C9A3 | — | final (ждёт upload) | TH_TEX_GRN_Plaster_a.png + _n/_r |
| TH_TEX_GRN_Wood | Текстура GRN_Wood (planks) | texture | 1.1 | tools/gen_textures.py | 512×512 | #6B4A2E | — | final (ждёт upload) | TH_TEX_GRN_Wood_a.png + _n/_r |
| TH_TEX_GRN_Terracotta | Текстура GRN_Terracotta (brick) | texture | 1.1 | tools/gen_textures.py | 512×512 | #A55A35 | — | final (ждёт upload) | TH_TEX_GRN_Terracotta_a.png + _n/_r |
| TH_TEX_GRN_StrawThatch | Текстура GRN_StrawThatch (thatch) | texture | 1.1 | tools/gen_textures.py | 512×512 | #C2A35C | — | final (ждёт upload) | TH_TEX_GRN_StrawThatch_a.png + _n/_r |
| TH_TEX_GRN_Stone | Текстура GRN_Stone (stone) | texture | 1.1 | tools/gen_textures.py | 512×512 | #8A8578 | — | final (ждёт upload) | TH_TEX_GRN_Stone_a.png + _n/_r |
| TH_TEX_GRN_OliveCanvas | Текстура GRN_OliveCanvas (canvas) | texture | 1.1 | tools/gen_textures.py | 512×512 | #5A6B3C | — | final (ждёт upload) | TH_TEX_GRN_OliveCanvas_a.png + _n/_r |
| TH_TEX_NET_SailCanvas | Текстура NET_SailCanvas (canvas) | texture | 1.1 | tools/gen_textures.py | 512×512 | #E8DCC0 | — | final (ждёт upload) | TH_TEX_NET_SailCanvas_a.png + _n/_r |
| TH_TEX_NET_ShipHull | Текстура NET_ShipHull (planks) | texture | 1.1 | tools/gen_textures.py | 512×512 | #4A3226 | — | final (ждёт upload) | TH_TEX_NET_ShipHull_a.png + _n/_r |
| TH_TEX_NET_DarkWoodUI | Текстура NET_DarkWoodUI (planks) | texture | 1.1 | tools/gen_textures.py | 512×512 | #3A2A1C | — | final (ждёт upload) | TH_TEX_NET_DarkWoodUI_a.png + _n/_r |

## Hero-модели (v1.3, Blender → FBX, D-011)
| ID | Название | Кат. | Вер. | Источник | Три. | Палитра | LOD | Статус | Файл |
|---|---|---|---|---|---|---|---|---|---|
| TH_ARK_House_00 | Hero-модель arkwain / house v0 | building | 1.3 | blender/hero_export.py | 6222 tri (L1 2798 / L2 1458) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/arkwain/TH_ARK_House_00.fbx |
| TH_ARK_House_01 | Hero-модель arkwain / house v1 | building | 1.3 | blender/hero_export.py | 6422 tri (L1 2888 / L2 1616) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/arkwain/TH_ARK_House_01.fbx |
| TH_ARK_House_02 | Hero-модель arkwain / house v2 | building | 1.3 | blender/hero_export.py | 6222 tri (L1 2798 / L2 1458) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/arkwain/TH_ARK_House_02.fbx |
| TH_ARK_Tower_00 | Hero-модель arkwain / tower v0 | building | 1.3 | blender/hero_export.py | 7212 tri (L1 3244 / L2 1772) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/arkwain/TH_ARK_Tower_00.fbx |
| TH_ARK_Workshop_00 | Hero-модель arkwain / workshop v0 | building | 1.3 | blender/hero_export.py | 5250 tri (L1 2362 / L2 1110) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/arkwain/TH_ARK_Workshop_00.fbx |
| TH_ARK_Manor_00 | Hero-модель arkwain / manor v0 | building | 1.3 | blender/hero_export.py | 10156 tri (L1 4570 / L2 2692) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/arkwain/TH_ARK_Manor_00.fbx |
| TH_ARK_Warehouse_00 | Hero-модель arkwain / warehouse v0 | building | 1.3 | blender/hero_export.py | 2336 tri (L1 0 / L2 0) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/arkwain/TH_ARK_Warehouse_00.fbx |
| TH_VAL_House_00 | Hero-модель valmere / house v0 | building | 1.3 | blender/hero_export.py | 6638 tri (L1 2986 / L2 1486) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/valmere/TH_VAL_House_00.fbx |
| TH_VAL_House_01 | Hero-модель valmere / house v1 | building | 1.3 | blender/hero_export.py | 6910 tri (L1 3108 / L2 1656) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/valmere/TH_VAL_House_01.fbx |
| TH_VAL_House_02 | Hero-модель valmere / house v2 | building | 1.3 | blender/hero_export.py | 6638 tri (L1 2986 / L2 1486) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/valmere/TH_VAL_House_02.fbx |
| TH_VAL_Tower_00 | Hero-модель valmere / tower v0 | building | 1.3 | blender/hero_export.py | 7636 tri (L1 3436 / L2 1760) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/valmere/TH_VAL_Tower_00.fbx |
| TH_VAL_Workshop_00 | Hero-модель valmere / workshop v0 | building | 1.3 | blender/hero_export.py | 5610 tri (L1 2524 / L2 1170) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/valmere/TH_VAL_Workshop_00.fbx |
| TH_VAL_Manor_00 | Hero-модель valmere / manor v0 | building | 1.3 | blender/hero_export.py | 10868 tri (L1 4890 / L2 2728) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/valmere/TH_VAL_Manor_00.fbx |
| TH_VAL_Warehouse_00 | Hero-модель valmere / warehouse v0 | building | 1.3 | blender/hero_export.py | 2336 tri (L1 0 / L2 0) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/valmere/TH_VAL_Warehouse_00.fbx |
| TH_GRE_House_00 | Hero-модель greenwald / house v0 | building | 1.3 | blender/hero_export.py | 6834 tri (L1 3074 / L2 1560) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/greenwald/TH_GRE_House_00.fbx |
| TH_GRE_House_01 | Hero-модель greenwald / house v1 | building | 1.3 | blender/hero_export.py | 7106 tri (L1 3196 / L2 1730) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/greenwald/TH_GRE_House_01.fbx |
| TH_GRE_House_02 | Hero-модель greenwald / house v2 | building | 1.3 | blender/hero_export.py | 6834 tri (L1 3074 / L2 1560) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/greenwald/TH_GRE_House_02.fbx |
| TH_GRE_Tower_00 | Hero-модель greenwald / tower v0 | building | 1.3 | blender/hero_export.py | 7920 tri (L1 3564 / L2 1890) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/greenwald/TH_GRE_Tower_00.fbx |
| TH_GRE_Workshop_00 | Hero-модель greenwald / workshop v0 | building | 1.3 | blender/hero_export.py | 5718 tri (L1 2572 / L2 1188) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/greenwald/TH_GRE_Workshop_00.fbx |
| TH_GRE_Manor_00 | Hero-модель greenwald / manor v0 | building | 1.3 | blender/hero_export.py | 11344 tri (L1 5104 / L2 2890) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/greenwald/TH_GRE_Manor_00.fbx |
| TH_GRE_Warehouse_00 | Hero-модель greenwald / warehouse v0 | building | 1.3 | blender/hero_export.py | 2336 tri (L1 0 / L2 0) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/greenwald/TH_GRE_Warehouse_00.fbx |
| TH_SHIP_Light | Hero-модель ships / ship_light v0 | building | 1.3 | blender/hero_export.py | 1062 tri (L1 0 / L2 0) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/ships/TH_SHIP_Light.fbx |
| TH_SHIP_Medium | Hero-модель ships / ship_medium v0 | building | 1.3 | blender/hero_export.py | 1296 tri (L1 0 / L2 0) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/ships/TH_SHIP_Medium.fbx |
| TH_SHIP_Heavy | Hero-модель ships / ship_heavy v0 | building | 1.3 | blender/hero_export.py | 1554 tri (L1 0 / L2 0) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/ships/TH_SHIP_Heavy.fbx |
| TH_WALL_Segment_01 | Hero-модель ships / wall_segment v0 | building | 1.3 | blender/hero_export.py | 536 tri (L1 0 / L2 0) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/ships/TH_WALL_Segment_01.fbx |
| TH_WALL_Gate_01 | Hero-модель ships / wall_gate v0 | building | 1.3 | blender/hero_export.py | 780 tri (L1 0 / L2 0) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/ships/TH_WALL_Gate_01.fbx |
| TH_DOCK_Pier_01 | Hero-модель ships / pier v0 | building | 1.3 | blender/hero_export.py | 284 tri (L1 0 / L2 0) | палитра DESIGN_TOKENS | L0/L1/L2 | exported FBX, ждёт импорта | ThreeHorizons/blender/export/ships/TH_DOCK_Pier_01.fbx |

