# Ф5 · Roblox-каркас (кодовая база)

> **Цель:** собираемый Rojo-проект с деревом модулей, конфигами из данных, сетью, сохранениями и
> тестами. Игры в нём ещё нет — но всё, что будет, ставится на этот каркас.
> **Зависит от:** Ф1 (данные), Ф0 (preflight) · **Выход:** `rojo build` → `.rbxlx`, профиль, NetAPI, тесты · **Сессий:** 2–3
> **Канон:** `ARCHITECTURE.md`, `WORLD_NETWORK_ARCHITECTURE.md`, `SPECS_COMBINED.md` §SECURITY

## Правила фазы

- Модульно, без мегаскриптов; каждый модуль — одна ответственность, с тестом (Gate S-1).
- Сервер — единственный авторитет: клиент присылает намерение, сервер валидирует.
- Сеть через `NetAPI` с версией `v1:` и идемпотентными ключами (`txId`).
- Никаких прямых `Set` из клиента; прайсы и награды — только серверные.

## Шаги

### 5.1 · Rojo-проект
- **Действие:** `ROBLOX_IMPLEMENTATION/default.project.json`: `src/ServerScriptService` →
  `ServerScriptService`, `src/ReplicatedStorage/TH_Shared` → `ReplicatedStorage/TH_Shared`,
  `src/StarterPlayer` → `StarterPlayer`, `src/Workspace` → `Workspace`.
- **Готово, когда:** `rojo build -o build/TH_dev.rbxlx` собирается, Studio открывает плейс.

### 5.2 · Дерево модулей
- **Действие:** создать по `ARCHITECTURE.md` §1: `TH_Shared/{Config,Types,Util,Net}`,
  `TH_Server/{Main,Data,Economy,Ships,NPC,World,Security,Chat}`, `TH_Client/{ClientMain,Controllers}`.
- **Готово, когда:** все папки в `src/`, каждый модуль — заглушка с `-- @version` и описанием.

### 5.3 · Типы и стиль
- **Действие:** `Types.lua` (PlayerProfile, Ship, Good, Route, WeatherState), `--!strict` во всех
  модулях, стиль под StyLua; `selene.toml` (std=roblox).
- **Готово, когда:** `stylua --check` и `selene` чистые, `luau-compile` проходит.

### 5.4 · Утилиты
- **Действие:** `Signal.lua`, `TableUtil.lua`, `SeededRNG.lua` (mulberry32 — детерминизм зданий/облаков),
  `TimeUtil.lua` (unix/фазы).
- **Готово, когда:** на каждую утилиту есть тест в `tests/` (детерминизм RNG, копирование таблиц).

### 5.5 · Конфиги из данных (Ф1)
- **Действие:** `Config/Factions.lua`, `Goods.lua`, `Ships.lua`, `Palettes.lua`, `Weather.lua` —
  генерируются `tools/bundle_design.py` из JSON; руками не правятся (шапка-предупреждение).
- **Готово, когда:** `python -X utf8 tools/bundle_design.py` → `Config/Bundle.lua`
  содержит 12 блоков и проходит `luau-compile`; **тест на руку:** изменить значение
  в `GAME_DESIGN/*.json` → перегенерировать → значение в `Bundle.lua` изменилось;
  расхождений между JSON и Lua нет (сверка `tools/validate_design.py` → `DESIGN OK`).

### 5.6 · `NetAPI`
- **Действие:** обёртка над RemoteEvents: имена `v1:<Domain>:<Action>`, сериализация аргументов,
  серверный rate-limit (торговля 5/с, взаимодействие 10/с, чат 3/с), клиентский троттлинг.
- **Готово, когда:** тест «спам 100 событий → 95 отброшено» проходит; в Output нет ошибок.
- **Канон:** `WORLD_NETWORK_ARCHITECTURE.md` §5; `SPECS_COMBINED.md` §SECURITY 4.

### 5.7 · Bootstrap
- **Действие:** `Main.server.lua` создаёт `Remotes/`, `TH_World/`, инициализирует сервисы в
  фиксированном порядке и логирует `[TH] server online v0.1`; `ClientMain.client.lua` — `[TH] client online`.
- **Готово, когда:** Play в Studio даёт обе строки, ноль ошибок.

### 5.8 · Профиль игрока
- **Действие:** `PlayerData.lua` (ProfileService-lite): схема `{version, faction, hero, money,
  skills{}, ships[], cargo{}, property[], quests{}, mapFog{}}`, autosave 120 с, save-on-leave,
  `BindToClose` с очередью, ретраи 3× с backoff, `Migrations.lua`.
- **Готово, когда:** leave/rejoin сохраняет деньги и фракцию; ручной тест на 2 клиентах.
- **Канон:** `ARCHITECTURE.md` §4.

### 5.9 · Безопасность
- **Действие:** `Validators.lua` (тип, диапазон, владение, кулдаун, дистанция <40 st),
  `RateLimit.lua`, `Audit.lua` (стратегические перемещения), `Wallet.lua` с транзакцией
  «списание+начисление в одной» и `txId`.
- **Готово, когда:** попытка списать больше баланса блокируется; повтор с тем же `txId` — no-op (тест).
- **Канон:** `SPECS_COMBINED.md` §SECURITY 1–8.

### 5.10 · Тестовый харнесс
- **Действие:** `tests/run.lua` под Luau CLI: набор юнит-тестов, код возврата ≠ 0 при провале;
  `tools/test.ps1`.
- **Готово, когда:** `tools/test.ps1` печатает `PASS=12 FAIL=0` (число растёт с модулями).

### 5.11 · Сборка и preflight
- **Действие:** `rojo build` в `build/TH_dev.rbxlx`, прогон `preflight.ps1` (stylua+selene+compile+build).
- **Готово, когда:** `PREFLIGHT OK`, `.rbxlx` открывается.

### 5.12 · Фиксация каркаса
- **Действие:** тег `v0.6.0`, бэкап, CHANGELOG, `STATUS.md` → «каркас готов».
- **Готово, когда:** новый человек по `docs/PIPELINE.md` (создаётся в Ф3.10) + `README` собирает проект с нуля.

## Definition of Done фазы

- [ ] Rojo собирает `.rbxlx`, Studio запускает без ошибок.
- [ ] NetAPI + rate-limit + тест спама.
- [ ] Профиль с autosave/rejoin/BindToClose/миграциями.
- [ ] Валидаторы, Wallet с `txId`, Audit.
- [ ] `tools/test.ps1` зелёный, `preflight` зелёный.
- [ ] Тег `v0.6.0`.

## Риски и грабли

- **Мегаскрипт «пока так»** — через месяц не разобрать. Сразу модули.
- **Сохранения без очереди на BindToClose** — потеря прогресса при рестарте сервера.
- **Доверие клиенту** — любая цена/награда с клиента = дюп. Только сервер.
- **Remote без версии** — ломает совместимость при обновлениях; сразу `v1:`.

## Чего в этой фазе НЕ делаем

- Геймплея (торговля «по-настоящему», квесты — Ф9), UI (Ф10), мира (Ф6).
- Кросс-шардовой синхронизации: только интерфейсы, реализация — после альфы.
