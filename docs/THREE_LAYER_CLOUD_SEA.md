# TH Cloud Sea — three moving strata

Визуализация «живого» облачного моря проекта: три слоя полупрозрачных текстурных плоскостей с дрейфом и покачиванием + мягкие альфа-пухи. Сейчас переведено в **GROUND TEST**-режим: море лежит на твёрдой тестовой площадке, чтобы его можно было осмотреть и обойти пешком.

## Ground test (текущий режим)

- Площадка: `Workspace.TH_TestGround` — 8×8 плит 2048×64×2048 (верх на Y=0), спавн `CloudTestSpawn` на (0, 1, 0), 4 маркера дистанции по X.
- Слои (клиентский LocalScript, 4 плитки 8192² на слой):

| Слой | Y, studs | Волна | Пухи | Роль |
|---|---:|---:|---:|---|
| Lower | 1.2 | 0.8 | 18 | Нижняя облачная плёнка у самой земли |
| Middle | 5.0 | 1.4 | 14 | Средний объём над землёй |
| Upper | 9.5 | 2.0 | 10 | Верхний ярус, видна панорама |

- Итого 12 текстурных тайлов + 42 биллоу, всё с `CanCollide/CanQuery/CanTouch = false`.
- Плитка = Part 2048×2×2048 + SpecialMesh Brick Scale (4,1,4) → footprint 8192²; Texture Face=Top, `StudsPerTileU/V = 4096`, отдельная скорость дрейфа.

## Sky layout (как было / для возврата)

Полный мир 54 000 × 78 000 studs: MAP_W=54000, MAP_D=78000, сетка 7 × 10 = 70 плиток на слой, слои Y = 430 / 250 / 70 (нижний к низам островов, средний и верхний — объём). Для возврата достаточно поменять `MAP_W, MAP_D` и Y-значения в `LAYERS` в `CloudSeaLayers.client.lua`.

## Файлы и рантайм

- Исходник: `ROBLOX_IMPLEMENTATION/src/StarterPlayer/TH_Client/CloudSeaLayers.client.lua`.
- Живой скрипт Studio: `StarterPlayer.StarterPlayerScripts.CloudSeaLayers` (LocalScript).
- Клиентская иерархия: `Workspace/TH_CloudSea_Layers/WaterStrata/{Lower,Middle,Upper}` + `CloudBillows`.
- Атрибуты корня: MapWidthStuds, MapDepthStuds, LayerCount=3, Layout="GroundTest".
- Освещение: Atmosphere Density 0.08 / Haze 0.45, Terrain.Clouds Cover 0.40, циклический день 14:42, туман 1500–14000.

## Текстуры (загружены в плейс)

Cloud sea: 130241582387781, 107842366949909, 128017488095902, 83368182906902.
Пухи: 103636435547948, 136330488657910, 88297930536668, 108873566412332.

## Проверка в Play

- Play на площадке: клиент построил 4 плитки на слой (12 всего), 42 пуха; лог `[TH CloudSea] ground test ready: 3 layers, 54 animated objects`.
- Позиции слоёв в рантайме: Lower ≈1.5, Middle ≈5.2, Upper ≈8.9 studs (с учётом покачивания).
- Персонаж стоит на твёрдой площадке (HRP y≈3), камера по умолчанию третьего лица; скриншот с фиксированной камеры показывает облачную поверхность на земле.
- В консоли есть старые предупреждения от legacy asset 203785492 (не связаны с облаками).
