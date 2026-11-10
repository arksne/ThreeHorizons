# NAMING — правила имён (v0.1)

> Один стиль на весь проект. Имя — это контракт: по нему работают реестр, поиск и генераторы.

## Ассеты

`TH_<FACTION>_<TYPE>_<VAR>` + суффикс LOD

| Часть | Значения | Пример |
|---|---|---|
| FACTION | `ARK`, `VAL`, `GRN`, `NET` (нейтральное), `PIR` | `TH_ARK` |
| TYPE | `House`, `Manor`, `Tower`, `Shop`, `Tavern`, `Workshop`, `Warehouse`, `Dock`, `Ship`, `Rock`, `Tree` | `TH_ARK_House` |
| VAR | `01`…`99` — вариант | `TH_ARK_House_02` |
| LOD | `_L1`, `_L2` (L0 без суффикса) | `TH_ARK_House_02_L1` |

Текстуры: `TH_TEX_<Material>_<map>.png`, где map = `a` (albedo), `n` (normal), `r` (roughness).
Пример: `TH_TEX_ARK_Stone_a.png`. Облачные: `TH_TEX_CloudPuff_00.png`, `TH_TEX_CloudSea_01.png`.

## Звук

`TH_AU_<faction>_<name>_v1` — например `TH_AU_ARK_hammer_v1`, `TH_AU_NET_wind_v1`.
Музыка: `TH_AU_MUS_<zone>_v1` (`ark`, `val`, `grn`, `port`, `sea`, `pirate`).

## Код (Luau)

- Модули: `PascalCase.lua` (`Wallet.lua`, `ShipService.lua`).
- Серверные скрипты: `Main.server.lua`; клиентские: `ClientMain.client.lua`, контроллеры `*Controller.lua`.
- Папки-сервисы: `TH_Server`, `TH_Shared`, `TH_Client`, `TH_World`, `TH_Art`, `TH_Templates`, `TH_Remotes`.
- События сети: `v1:<Domain>:<Action>` — `v1:Trade:Buy`, `v1:Ship:Anchor`.
- Поля профиля: `camelCase` (`money`, `quests`, `mapFog`).

## Данные (GAME_DESIGN)

- Файлы: `PascalCase.json` (`Factions.json`, `Goods.json`), кроме служебных: `constants.json`,
  `travel_times.json`, `bundle.json`.
- `id` внутри — `snake_case`: `arkvein`, `dark_wood`, `medium_hull`.
- Поля — `camelCase`: `basePrice`, `timeSec`, `strategic`.

## Документы и канвасы

- Фазы: `docs/roadmap/phase-XX-name.md`; канвасы фаз: `docs/roadmap/canvas/phase-XX.canvas`.
- Решения: `D-XXX` (лор/архитектура) и `S-XX` (стартовые решения).
- Версии: `v0.MAJOR.MINOR`, тег git = `v0.MAJOR.MINOR`, бэкап `backups/v0.MAJOR_<дата>`.

## Запрещено

- Русские имена файлов кода и ассетов, пробелы, `final_final_v2`.
- Дубли: одно имя — один объект (проверка `grep` перед добавлением).
- Менять имя без записи в `DECISIONS.md` — на имена ссылаются реестр и конфиги.
