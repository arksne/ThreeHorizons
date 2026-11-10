# tools — скрипты проекта

| Файл | Что делает |
|---|---|
| `make_roadmap_canvas.py` | собирает `ROADMAP_0.1.canvas` + канвасы фаз из `docs/roadmap/*.md` |
| `make_roadmap_html.py` | автономный HTML-просмотрщик индекса (без Obsidian) |
| `preview_roadmap.py` | PNG-превью любого `.canvas` (диагностика раскладки) |
| `preflight.ps1` | единая проверка: stylua + selene + luau-compile + rojo build (**Ф0.6**) |
| `validate_design.py` | валидатор `GAME_DESIGN/*.json` (**Ф1.12**) |
| `validate_world.py` | валидатор координат и маршрутов (**Ф2.6**) |
| `bump_version.py`, `backup.ps1` | версии и бэкапы (**Ф0.9**) |

## Правила

- Скрипты не зависят от текущей папки запуска (пути от `Path(__file__).parent.parent`).
- Всё, что генерируется, пишется в проект; никаких временных файлов в корне.
- Python запускать с `-X utf8`; сложные строки — только через файл, не `-c`.
