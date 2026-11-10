# STATUS — где мы сейчас

> Живой файл: одна страница «текущее состояние». История — `docs/CHANGELOG.md`, решения —
> `docs/DECISIONS.md`, план — `ROADMAP_0.1.md`, статусы шагов — `docs/PROGRESS.json`.
> Обновлён: **2026-11-10**.

## Текущая фаза

Закрыты: **Ф0** (12/12) и **Ф1** (13/13). Следующая — **Ф2 · Масштаб и геометрия мира**.

## Ф0 · База и правила — закрыта

Скелет папок, `.gitignore`, `tools/preflight.ps1` (+ `-Art`), `tools/TOOLCHAIN.md`,
`docs/STATUS.md` / `CHANGELOG.md` / `DECISIONS.md` / `NAMING.md` / `SESSION_TEMPLATE.md`,
`docs/PROGRESS.json`, `tools/bump_version.py`, `tools/backup.ps1`, `version.json`,
`ROBLOX_IMPLEMENTATION/default.project.json` + `build/TH_dev.rbxlx`.
Решения **S-01…S-06** приняты и записаны.

## Ф1 · Канон → данные — закрыта

| Артефакт | Что внутри |
|---|---|
| `docs/roadmap/canon-map.md` | 53 строки «источник → JSON → поле» |
| `GAME_DESIGN/Factions.json` | 3 фракции + Эстерхольм + Чёрная Гавань (с чёрным рынком), палитры, районы game/lore |
| `GAME_DESIGN/Heroes.json` | 3 пары М/Ж, возрасты, крючки, точка встречи |
| `GAME_DESIGN/Goods.json` | 14 товаров, 5 цепочек, 3 стратегических ресурса |
| `GAME_DESIGN/Prices.json` | цены корпусов/товаров, чёрный рынок (всё PROPOSED) |
| `GAME_DESIGN/Ships.json` | 3 корпуса, 10 модулей, 6 ролей экипажа |
| `GAME_DESIGN/Professions.json` | 12 навыков с уровнями |
| `GAME_DESIGN/Routes.json` | 4 маршрута + пиратский рейд (расстояния — Ф2.7) |
| `GAME_DESIGN/Buildings.json` | 8 классов зданий с бюджетами |
| `GAME_DESIGN/Weather.json` | 4 состояния + эффекты |
| `GAME_DESIGN/NPC.json`, `Quests.json` | 5 NPC с расписанием, 3 стартовых квеста |
| `GAME_DESIGN/constants.json` | масштаб, эргономика, лимиты, UI, облака, поражение |
| `GAME_DESIGN/bundle.json` + `Config/Bundle.lua` | собранный бандл для Luau |
| `tools/validate_design.py`, `tools/bundle_design.py` | валидатор (12 файлов) и сборка бандла |

Решения **C-10 / C-11** приняты (районы — по CITY_LAYOUTS; Гавань — пираты + торговля + чёрный рынок).

## Проверено фактически

- `tools/validate_design.py` → **DESIGN OK**; негативный тест (битый JSON) падает с понятной ошибкой.
- `tools/bundle_design.py` → `bundle.json` + `Bundle.lua` (12 блоков), `luau-compile` проходит.
- `pwsh -File tools/preflight.ps1` → **PREFLIGHT OK** (stylua, selene, luau-compile, rojo build).
- Git: теги `v0.1.0` (Ф0) и `v0.2.0` (Ф1), бэкапы `backups/v0.1.0_2026-11-10`, `backups/v0.2.0_2026-11-10`.
- **История переписана 2026-11-10** (см. CHANGELOG): из git вычищены находки v1.x (63 FBX, 66 текстур,
  .blend, Luau-модули, атласы) — 184 МБ. `.git` 167 МБ → 0.8 МБ, в истории только канон v0.1 (123 файла).
  **Хеши коммитов и тегов изменились**, старые SHA недействительны. Бэкап старой истории:
  `../_git_cleanup/ThreeHorizons_full_backup_2026-11-10.bundle`. Старые файлы лежат на диске:
  `../_TRASH_2026-11-10/` и `../_ThreeHorizons_archive_2026-11-10/`.
- **Роадмап доведён до проверяемого состояния** (2026-11-10): у всех **147 шагов** есть критерий
  «готово, когда» — команда, измеримое число или тест (было 41 без проверки); битых ссылок в
  фазах — 0; канвасы и HTML пересобраны; `MASTER_SCALE_SPEC.md` §1/§5 приведён к S-01/S-02;
  решения C-01…C-12 сведены в `DECISIONS.md`; рамка карты зафиксирована как **S-07**.

## Следующее (Ф2)

**2.1** константы масштаба (3.571 studs/м, сжатие 1:10) → **2.2** координаты 6 островов →
**2.3** мини-острова → **2.4** высоты → **2.5** карта → **2.6** валидатор геометрии →
**2.7** времена перелётов → **2.8** кварталы Аркенхольда → **2.9** blockout-прикидка → **2.10** фиксация.

## Открытые вопросы

Нет. C-01…C-12 закрыты, S-01…S-07 приняты.

## Известные риски

- **selene** работает с `std = "lua51"` (roblox-std требует сети/записи в `%LOCALAPPDATA%`);
  `undefined_variable` отключён, API-ошибки ловит `luau-compile`. Вернуть `roblox` при появлении сети.
- **Blender** не в проекте — восстановить из `../_ThreeHorizons_archive_2026-11-10/tools/blender/` в Ф3.1.
- **Roblox Studio** — подключение в Ф6.
