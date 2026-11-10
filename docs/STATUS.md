# STATUS — где мы сейчас

> Живой файл: одна страница «текущее состояние». История изменений — `docs/CHANGELOG.md`,
> решения — `docs/DECISIONS.md`, план — `ROADMAP_0.1.md`.
> Обновлён: **2026-11-10**.

## Текущая фаза

**Ф0 · База и правила** — шаги 0.1–0.12. Статусы — в `docs/PROGRESS.json` (канвас красится из него).

| Шаг | Статус | Evidence |
|---|---|---|
| 0.1 Скелет папок | ✅ | `GAME_DESIGN/`, `ART_ASSETS/{models,textures,previews}`, `ROBLOX_IMPLEMENTATION/{src,tests,build}`, `STEAM_IMPLEMENTATION/`, `tests/`, `backups/` + README в каждой |
| 0.2 `.gitignore` | ✅ | бинарники арта, build, бэкапы, вендорные тулзы исключены |
| 0.3 Коммит + тег | ✅ | `e52efa7`, тег `v0.1.0` |
| 0.4 Инвентаризация | ✅ | `tools/TOOLCHAIN.md` |
| 0.5 Тулчейн | ✅ | Luau CLI восстановлен в `tools/luau/`; Rojo/selene/StyLua найдены в `D:\DSH\20-tools` |
| 0.6 `preflight.ps1` | ✅ | `PREFLIGHT OK` на пустом src |
| 0.7 Документы управления | ✅ | `STATUS.md`, `CHANGELOG.md`, `DECISIONS.md` приведены к формату |
| 0.8 Правила имён | ✅ | `docs/NAMING.md` |
| 0.9 Версии и бэкапы | ✅ | `tools/bump_version.py`, `tools/backup.ps1`, `version.json` |
| 0.10 Шаблон сессии | ✅ | `docs/SESSION_TEMPLATE.md` |
| 0.11 Решения S-01…S-06 | ✅ | записаны в `DECISIONS.md`, подтверждены владельцем 2026-11-10 |
| 0.12 Пустой плейс | ✅ | `ROBLOX_IMPLEMENTATION/build/TH_dev.rbxlx` собран Rojo |

## Проверено фактически

- `pwsh -File tools/preflight.ps1` → `PREFLIGHT OK`.
- `rojo build` собирает `TH_dev.rbxlx` из `default.project.json`.
- Git: `v0.1.0` + рабочие коммиты по шагам.

## Следующее

**Ф1 · Канон → данные**: 12 JSON в `GAME_DESIGN/`, валидатор, `bundle.json`.

## Открытые вопросы

Нет. Решения S-01…S-06 приняты: 1 м = 3.571 studs, сжатие 1:10, карта 18×26 км, шард 60,
вода near-зоной, облака — три слоя.

## Известные риски

- Blender не в проекте (восстановить из `../_ThreeHorizons_archive_2026-11-10/tools/blender/` в Ф3.1).
- Roblox Studio подключается только в Ф6 (MCP), до этого все проверки офлайн.
