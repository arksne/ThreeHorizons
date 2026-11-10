# TOOLCHAIN — инструменты проекта (v0.1)

> Зафиксировано: 2026-11-10. Проверено фактически (запуск + версия).
> Правило: скрипты не полагаются на `PATH` — разрешают путь из таблицы ниже.

| Инструмент | Версия | Путь | Где используется |
|---|---|---|---|
| **git** | 2.47.0.windows.2 | `C:\Program Files\Git\cmd\git.exe` | версии, теги, бэкапы |
| **Python** | 3.12.4 | `C:\Users\ARK\AppData\Local\Programs\Python\Python312\python.exe` | все `tools/*.py` (всегда `-X utf8`) |
| Python (резерв) | bundled DSH | `C:\Users\ARK\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe` | если системный недоступен |
| **Node** | 22.14.0 | `C:\Program Files\nodejs\node.exe` | проверка JS, обслуживание HTML-канваса |
| **Rojo** | 7.7.1 | `D:\DSH\20-tools\rojo\rojo.exe` | сборка `.rbxlx` из `ROBLOX_IMPLEMENTATION/src` |
| **selene** | 0.32.0 | `D:\DSH\20-tools\selene\selene.exe` | линт Luau (std=roblox) |
| **StyLua** | 2.6.0 | `D:\DSH\20-tools\stylua\stylua.exe` | формат Luau |
| **Luau CLI** | 0.745 | `tools/luau/luau.exe`, `tools/luau/luau-compile.exe` | офлайн-тесты и компиляция модулей |
| **Blender** | 4.5.15 LTS | портативный — `../_ThreeHorizons_archive_2026-11-10/tools/blender/` | арт-пайплайн; восстановить в `tools/blender/` в **Ф3.1** |
| **Obsidian** | 1.15.0 | `C:\Users\ARK\AppData\Local\Programs\Obsidian\Obsidian.exe` | только просмотр канвасов |
| **Roblox Studio** | — | через MCP-подключение | проверки в Play (`Ф6+`) |

## Важные оговорки

- **Rojo / selene / StyLua не в `PATH`** — вызываем по абсолютным путям (см. `tools/preflight.ps1`, Ф0.6).
  Добавлять глобально в `PATH` не обязательно и не рекомендуется: ломает воспроизводимость между сессиями.
- **Luau не в `PATH`** — бинарники лежат в `tools/luau/` (папка в `.gitignore`, восстановлена из архива).
- **Blender тяжёлый (~900 МБ)** и в git не попадает: восстанавливаем копированием из архива перед Ф3.
- **Python:** inline `python -c` со сложными кавычками на этой машине ломается — только через `.py`-файл.
- Версии меняются только записью в `docs/DECISIONS.md` (иначе «на другой машине не собирается»).

## Проверка тулчейна

```powershell
pwsh -File tools/preflight.ps1          # появится в Ф0.6
```

## История

| Дата | Изменение |
|---|---|
| 2026-11-10 | Инвентаризация: git/python/node/rojo/selene/stylua/luau/obsidian на месте; Blender — восстановить в Ф3 |
