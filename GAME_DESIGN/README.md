# GAME_DESIGN — чистые правила игры

Данные и правила **без Roblox-зависимостей**: JSON (источник) + сгенерированные Luau-таблицы.
Создаётся в **Ф1**: `Factions.json`, `Heroes.json`, `Goods.json`, `Prices.json`, `Ships.json`,
`Professions.json`, `Routes.json`, `Buildings.json`, `Weather.json`, `NPC.json`, `Quests.json`,
`constants.json`, `travel_times.json`, `bundle.json`.

## Правила

- Один документ канона → один файл; в каждом поле `sources` со ссылкой на `docs/<файл>#<раздел>`.
- Никакой логики: только значения и `id`-ссылки. Формулы — в коде (`ROBLOX_IMPLEMENTATION`).
- Спорные числа помечаются `"status": "PROPOSED"` и становятся `APPROVED` только после гейм-теста.
- Правится руками или генератором; в игре используется `bundle.json` → `Config/Bundle.lua`.

Канон: `docs/THREE_HORIZONS_PROJECT_BIBLE.md` §6, `docs/BALANCING_SPEC.md`, `docs/world/*`.
