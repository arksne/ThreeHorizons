# PROCEDURAL GENERATION SYSTEM (APPROVED v0.1)
> Движконезависимое ядро (таблицы боксов) + адаптеры (Roblox Builder / Blender bpy).

## Принцип
1. `BuildingGenerator.generate(params)` возвращает GenResult в метрах — чистые данные, без Roblox API. Детерминизм: seed → одно здание везде (mulberry32).
3. Бюджет L0: дом ≤60 боксов. Декор CanCollide=false. Magenta = токен не из палитры (frog).

## Генераторы (статус)
- BuildingGenerator — DONE (house/tower/workshop, Арквейн). Параметры: faction/width/depth/floors/floorH/roof/seed/kind.
- ArchitectureGenerator — PROPOSED v0.2 (стены/арки/лестницы/крыши-наборы из каталога §единый каталог деталей).
- ShipGenerator — PROPOSED v0.2 (корпус по Hulls + модули; интерьер обязателен).
- InteriorGenerator / EnvironmentGenerator / DecorationGenerator — PROPOSED v0.3 (мебель/острова/фонари) после утверждения Bible.

## Вариативность без хаоса (Арквейн)
Фасад всегда +Z, дверь 1.0×2.1, окна 0.9×1.2 шаг ~1.8м, балки 0.24, пояс между этажами, крыша gable/hip/tower/flat, медь-оковка + бордо-акцент. Seed двигает только смещение двери и высоту крыши в допуске — силуэт улицы целостен.

## QA
`tests/test_building_generator.lua` (создаётся в Ф5): детерминизм, бюджет, дверь, окна, имена TH_*. Builder проверяется magenta-сканом.
