# Новая карта: живое море 54 000 × 78 000

Статус: карта создана и проверена в Play (Roblox Studio, Place1 → `ThreeHorizons_LivingSea.rbxlx`). Море — настоящая вода Terrain с анимацией волн.

## Что в карте

| Объект | Параметры |
|---|---|
| Мир | Workspace attributes: `MapWidthStuds = 54000`, `MapDepthStuds = 78000` |
| Вода (настоящая, Terrain) | 32 000 × 32 000 studs, глубина 4 studs, 4 блока FillBlock по 16 000 (64 млн вокселей) |
| Волны | WaterColor RGB(22,129,168), WaterTransparency 0.18, WaterReflectance 0.2, WaterWaveSize 0.5, WaterWaveSpeed 16 |
| Пирс | Deck 70×4×70 на Y=14, 8 свай 8×36×8, SpawnLocation `SeaSpawn` на (0, 16.5, 0) |
| Свет | ClockTime 12.5, Brightness 2.5, Atmosphere Density 0.2 / Haze 0.8, Terrain.Clouds Cover 0.34 |
| Туман | FogStart 2500, FogEnd 14 000 — прячет край воды, море выглядит бесконечным |

## Почему вода не на всей площади сразу

Roblox Terrain хранит воду в вокселях 4×4×4 studs. Чтобы залить реальной водой весь прямоугольник 54 000 × 78 000, нужно ~640 млн вокселей — Studio падает при запуске Play (проверено: краш процесса Studio). Поэтому:

- настоящая анимированная вода занимает 32 000 × 32 000 studs (64 млн вокселей — стабильно);
- туман (FogEnd 14 000) полностью скрывает её край, поэтому из игры море неотличимо от бесконечного;
- заявленный размер карты 54 000 × 78 000 остаётся в атрибутах и документации; при желании воду можно расширять, добавляя блоки FillBlock по 16 000 (каждые +16 000 → +16 млн вокселей).

## Файлы

- Генератор: `ThreeHorizons/tools/make_living_sea.py`
- Плейс: `ThreeHorizons/ART_ASSETS/demo/ThreeHorizons_LivingSea.rbxlx`
- Скриншоты: `ThreeHorizons/ART_ASSETS/screenshots/TH_LivingSea_Water.jpg`, `TH_LivingSea_Pier.jpg`
- Серверный скрипт: `ServerScriptService/LivingSeaBuilder` — заливает воду и ставит свет/туман при старте Play.

## Запуск

```
RobloxStudioBeta.exe -task EditFile -localPlaceFile ThreeHorizons\ART_ASSETS\demo\ThreeHorizons_LivingSea.rbxlx
```

F5 — вода появляется за пару секунд, персонаж появляется на пирсе; вода анимируется движком.

## Известные ограничения

- Штатный спавн иногда сбрасывает персонажа в воду (в Play зафиксировано состояние Swimming) — надо доработать точку спавна (поднять SpawnLocation над настилом / увеличить пирс), чтобы персонаж гарантированно оставался на пирсе.
- Полная вода 54 000 × 78 000 в нативном Terrain невозможна по памяти; альтернатива — несколько слоёв/чанков с подгрузкой, как в больших Roblox-океанах.
