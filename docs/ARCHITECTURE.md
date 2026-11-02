# ARCHITECTURE — Roblox-проект Three Horizons (APPROVED v0.1)
> Модульно, без мегаскриптов. Чистые правила — в GAME_DESIGN, адаптер Roblox — здесь.

## 1. Дерево (фактическое, создать импортом)
```
ReplicatedStorage/TH_Shared/
  Config/        Factions.lua, Ships.lua, Goods.lua, TravelTimes.lua, Palettes.lua
  Types/         Types.lua (Luau strict types)
  Util/          Signal.lua, TableUtil.lua, SeededRNG.lua
  Net/           NetAPI.lua (обёртка над RemoteEvents, имена событий, rate-limit клиента)
  Remotes/       (папка RemoteEvents — создаются bootstrap-скриптом)
ServerScriptService/TH_Server/
  Main.server.lua
  Data/          ProfileService-lite: PlayerData.lua, DataSchema.lua, Migrations.lua
  Economy/       Wallet.lua, Shops.lua, Production.lua, Audit.lua
  Ships/         ShipService.lua, CrewService.lua, FleetOffline.lua
  NPC/           NPCService.lua, Schedules.lua
  World/         WorldEvents.lua, WeatherService.lua, DayNight.lua
  Security/      Validators.lua, RateLimit.lua
  Chat/          FilteredChat.server.lua (обёртка TextService:FilterStringAsync)
ServerStorage/TH_Templates/  (модели кораблей/NPC — подкладываются генераторами)
StarterPlayer/TH_Client/
  ClientMain.client.lua, Controllers/: ShipController, Interaction, MapUI, TradeUI, CrewUI, FleetUI, Settings
Workspace/TH_World/  (чанки: TH_Arkwayn, TH_Valmere, TH_Greenwald, TH_Sky)
```

## 2. Системы (список, APPROVED)
Персонаж/профессии, корабли+флот+офлайн, интерьеры, NPC-расписания, экономика+производство, собственность, мультиплеер/соц, сюжет/события, погода/время суток, карта/стриминг, UI-пак, звук, аналитика, live-ops, релиз.

## 3. Сеть (7030-символьно кратко, полное — WORLD_NETWORK_ARCHITECTURE.md)
- Авторитет сервера на всё ценное (баланс, владение, грузы, награды). Клиент — только запрос намерения.
- RemoteEvents через NetAPI с версионированием (`v1:`), идемпотентными ключами (защита от дублей наград).
- RateLimit серверный: торговля 5/с, взаимодействие 10/с, чат 3/с.
- Мир логически един: DataStore + MemoryStore (аренда событий/аукционов) + MessagingService (кросс-серверные события: погода, нападения, контракты). Физически — шарды по 60–80 игроков, TeleportService между хабами.

## 4. Сохранения
Profile: {version, faction, hero, money, skills{}, ships[], cargo{}, property[], quests{}, mapFog{}}.
DataStoreService: autosave 120 с + save-on-leave (BindToClose с очередью), ретраи 3× с backoff, версионирование + миграции, pcall-обёртки, аудит экономики. Потеря прогресса запрещена классом (двойная запись критичных транзакций).

## 5. Оптимизация (кратко, полное — OPTIMIZATION_PLAN.md)
StreamingEnabled + чанки + LOD + CanCollide только рядом + кэширование NPC + бюджет: ≤ 8k parts near, ≤ 60 Remote/с на игрока, свет — 1 Directional + локальные.

## 6. Зависимости этапов (APPROVED)
Bible(0) → Scale/Tokens/Map(1) → Registry/Generators(2) → Арквейн-блокout(3) → персонаж/корабли(4) → NPC/интерьеры(5) → экономика(6) → соц/сеть(7) → сюжет(8) → звук/баланс(9) → оптимизация/QA/релиз(10).
