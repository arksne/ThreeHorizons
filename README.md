# THREE HORIZONS — Project Root
> Единый живой мир, а не набор городов и систем. Single Source of Truth: `docs/THREE_HORIZONS_PROJECT_BIBLE.md`.

## Одна главная папка (APPROVED)
Всё хранится здесь, в `ThreeHorizons/`:
```
ThreeHorizons/
  docs/                  # вся документация и библии (SSOT — Bible)
  GAME_DESIGN/           # движконезависимые правила (механики, экономика, баланс — JSON/Lua-таблицы)
  ART_ASSETS/            # исходники: Blender, текстуры, палитры, реестр ассетов
  ROBLOX_IMPLEMENTATION/ # только Roblox: Luau, Studio-сборка, UI, сеть, сохранения
  STEAM_IMPLEMENTATION/  # заглушка под будущий движок (только GDD-интерфейсы, без кода)
  blender/               # Blender Python-генераторы и экспортные пресеты
  tools/                 # импорт в Studio, валидаторы, сборка карт
  tests/                 # тесты Luau + чеклисты QA
  backups/               # снапшоты Bible и карт (не перезаписывать молча)
  _refs/                 # 9 концепт-атласов (ref01..ref09.png) — только референс, не модель
```

## Правила (кратко)
1. Лор из Bible со статусом APPROVED не меняется без записи в `DECISIONS.md` + `CHANGELOG.md`.
2. Масштаб: только `docs/MASTER_SCALE_SPEC.md`. Случайных масштабов нет.
3. Цвет/материал: только `docs/DESIGN_TOKENS.md`. Новый ассет проходит худконтроль (см. `QUALITY_ASSURANCE.md`, gate A-1).
4. Никаких дублей моделей: перед созданием — поиск в `docs/ASSET_REGISTRY.md`.
5. Roblox-код не смешивается с `GAME_DESIGN/` (чистые правила) — адаптеры живут в `ROBLOX_IMPLEMENTATION/`.
6. Не выдавать концепт за модель: статус ассета `concept | blockout | final | lod`.

## Статус сейчас
Этап 0 — Bible + каркас + первый генератор Арквейна. Массовая генерация моделей и систем — только после утверждения Bible (по вашему указанию).
