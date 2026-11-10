# ROBLOX_IMPLEMENTATION — код игры

| Папка | Что лежит |
|---|---|
| `src/` | исходники Luau, собираются Rojo в `.rbxlx` |
| `tests/` | тесты Luau CLI (офлайн, без Studio) |
| `build/` | собранные плейсы (в git не коммитим) |

## Структура образа (создаётся в Ф5)

```
src/
  ServerScriptService/TH_Server/    Main, Data, Economy, Ships, NPC, World, Security, Chat
  ReplicatedStorage/TH_Shared/      Config, Types, Util, Net
  StarterPlayer/TH_Client/          ClientMain, Controllers, UI
```

## Правила

- Модульно, без мегаскриптов; один модуль — одна ответственность, у каждого тест.
- Сервер — единственный авторитет: клиент шлёт намерение, сервер валидирует.
- Сеть через `NetAPI`: события `v1:<Domain>:<Action>`, идемпотентность по `txId`.
- Сборка: `rojo build -o build/TH_dev.rbxlx`; проверка: `pwsh -File tools/preflight.ps1`.

Канон: `docs/ARCHITECTURE.md`, `docs/WORLD_NETWORK_ARCHITECTURE.md`, `docs/SPECS_COMBINED.md` §SECURITY.
