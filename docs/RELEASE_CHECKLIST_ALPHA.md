# RELEASE CHECKLIST — Закрытая альфа (APPROVED v1.0)
> Критерии R-1: всё ниже отмечено evidence перед инвайтами 50–100 игроков.

## A. Импорт и запуск (Studio, владелец)
- [ ] `tools/import_to_studio.lua` в Command Bar → дерево 41+ модулей создано (теперь 45+ с WorldAssembler/LOD/CrossShard/Analytics/Chat)
- [ ] Main (Script) + ClientMain (LocalScript) созданы вручную, код вставлен 1-в-1
- [ ] Output при старте: `[TH] server online v0.3`, клиент `[TH] client online v0.3`, ошибок 0
- [ ] `TH_World` Folder создан; `WorldAssembler.assembleAll(TH_World)` → summary в Output

## B. Тесты (Command Bar, все 6 файлов — PASS)
- [ ] test_building_generator.lua — детерминизм, бюджет ≤60, дверь 1.0×2.1
- [ ] test_arch_ship.lua — арка 7 частей, 3 корпуса с рубкой/двигателем/каютой, overmass ловится
- [ ] test_district_fleet.lua — квартал, флот прибыл, 6 героев
- [ ] test_economy.lua — кошелёк-дубли, лимиты, производство, собственность, контракты, гильдия, квест
- [ ] test_factions_client.lua — палитры, здания 3 фракций, акведук/мельница, 5+7 сайтов, стриминг-состояния
- [ ] test_fullworld.lua — estimate 12 сайтов, CAS claim/release, analytics snapshot

## C. Мир и бюджеты
- [ ] 12 сайтов собраны, summary: models/parts записать сюда: _____ / _____
- [ ] near-чанки ≤8000 parts (Streaming.countParts на самом тяжёлом): _____
- [ ] LOD: LODBuilder.makeLOD на доме/корабле, savedPct ≥25%: _____
- [ ] Blender batch (у владельца): 13/13 FBX + manifest.txt

## D. Геймплей-сквозняк (2 клиента + сервер)
- [ ] Спавн → выбор фракции/героя → Эстерхольм → квест vale_start сдан (txId, без дубля)
- [ ] Покупка дерева → производство досок → продажа; strategic-лимит проверен
- [ ] Создание корабля → экипаж → dispatch → прибытие тиком
- [ ] Контракт взять/сдать; участок купить; гильдия+склад; сообщение через фильтр
- [ ] Погода-фаза меняется, событие публикуется кросс-шард (или fallback-push)
- [ ] Leave/rejoin: профиль, деньги, грузы, квест на месте

## E. Откат
- [ ] Бэкап `backups/v1.0_*` снят; тег релиза зафиксирован в CHANGELOG
- [ ] BindToClose досохранение проверено (остановить сервер в Studio — ошибок DataStore 0)

## Подписи
Владелец: ______________ Дата: __________ Версия Bible: v1.0
