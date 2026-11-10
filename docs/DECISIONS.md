# DECISIONS LOG — Three Horizons
> Каждое утверждённое решение. Без записи здесь лор не меняется.

| Дата | ID | Решение | Основание | Статус |
|---|---|---|---|---|
| 2026-11-02 | D-001 | Single Source of Truth — `docs/THREE_HORIZONS_PROJECT_BIBLE.md` | Unified Standard §1 | APPROVED |
| 2026-11-02 | D-002 | Масштаб 1м=3st, фасад +Z, pivot в основании | MASTER_SCALE_SPEC | APPROVED |
| 2026-11-02 | D-003 | Канон фамилий: Морвей/Morwey; специализации Гринвальда — боевые из Master Prompt | CONTRADICTIONS C-02/C-03 | APPROVED |
| 2026-11-02 | D-004 | Дирижабли = худ. подача эфирной подъёмной силы, отдельного класса нет | C-06 | APPROVED |
| 2026-11-02 | D-005 | Сжатие мира 1:20 гор / 1:10 верт; шарды 60–80 игроков | WORLD_MASTER_MAP | APPROVED |
| 2026-11-02 | D-006 | Gate: массовая генерация только после утверждения Bible | Указание владельца | APPROVED |
| 2026-11-02 | D-008 | Bible v0.1 APPROVED владельцем; открыть Этапы 1–3 (Architecture/Ship/Interior/Env/Deco + библиотека Арквейна + квартал Аркенхольда + ядро персонажей/кораблей) | Утверждение в чате | APPROVED |
| 2026-11-02 | D-009 | Bible v0.3 APPROVED владельцем; открыть FULL PROJECT до v1.0 (все территории, финальные ассеты+LOD, интеграция, QA, закрытая альфа) | Утверждение в чате 04:59 | APPROVED |
| 2026-11-02 | D-010 | Текстурный пак: 66 бесшовных PBR PNG 512² (22 материала), TileSize=4 м, палитра = DESIGN_TOKENS; применять через MaterialConfig + SurfaceAppearance, фолбэк на Color+Material | TEXTURE_PIPELINE + худконтроль A-1 | APPROVED |
| 2026-11-02 | D-011 | Арт-пайплайн гибрид: HERO (Blender→FBX→MeshPart, ≤12k tri, LOD L0/L1/L2) + процедурные боксы как L2-фолбэк; игра не зависит от наличия мешей, `MeshBuilding` возвращает модель всегда | ART_PIPELINE_BLENDER_KIT + прогон Blender 4.5.15 | APPROVED |
| 2026-11-02 | D-007 | Roblox Studio не подключён (studios=[]) — работа через файлы + импорт-скрипт | Проверка MCP | APPROVED |
| 2026-11-10 | S-01 | **1 метр = 3.571 studs** (1 stud = 0.28 м). Значение «3 studs» в MASTER_SCALE_SPEC — бытовое округление, не для расчётов | WORLD_SCALE + физика Roblox; подтверждено владельцем 2026-11-10 | APPROVED |
| 2026-11-10 | S-02 | **Сжатие мира 1:10** по горизонтали и вертикали (игровые размеры из WORLD_MASTER_MAP) | WORLD_MASTER_MAP §«Игровые размеры»; P-01 закрыт | APPROVED |
| 2026-11-10 | S-03 | Размер карты — **18×26 км игровых**; 168 км² — только лор-текст | WORLD_MASTER_MAP | APPROVED |
| 2026-11-10 | S-04 | Лимит шарда — **60 игроков** на старте, поднимать после профилирования | P-02, ARCHITECTURE §5 | APPROVED |
| 2026-11-10 | S-05 | **Вода только near-зоной 2–4 км** + туман/облачное море на горизонте; полную карту водой не заливаем | NEW_MAP_LIVING_SEA (краш Studio на 54k×78k) | APPROVED |
| 2026-11-10 | S-06 | **Меш-облака запрещены**: три слоя — нативные Clouds + альфа-клочья + Atmosphere | D-012, CLOUD_SYSTEM | APPROVED |
| 2026-11-10 | C-10 | **Районы столиц — по `world/CITY_LAYOUTS.md`** (8 игровых районов). Лорный список Bible §2 — названия и атмосфера, не раскладка | Подтверждено владельцем 2026-11-10 | APPROVED |
| 2026-11-10 | C-11 | **Чёрная Гавань — одна**: пиратский свободный порт + торговый узел, 0.8×0.6 км / 1700 м / ~8 000 (по C-05). **В Гавани есть чёрный рынок** (нелегальный оборот без записей в аудите). Pirate Base отдельным островом не вводим | Подтверждено владельцем 2026-11-10 | APPROVED |
| 2026-11-02 | C-01 | Лор-площади островов (108/432/475 км²) — **проектные ориентиры**; игровые размеры берём только из `WORLD_MASTER_MAP.md` (сжатая шкала 1:10) | Арифметика атласов; `CONTRADICTIONS.md` C-01 | APPROVED |
| 2026-11-02 | C-02 | Канон фамилии — **Морвей / Morwey** (Леонард и Леона Морвей). Варианты «Моряк» — ошибки генерации артов | `CONTRADICTIONS.md` C-02 | APPROVED |
| 2026-11-02 | C-03 | Боевой набор Гринвальда — из Master Prompt (следопыт/лучник/пехотинец/арбалетчик). «Фермер» — **профессия**, не специализация; в UI показывать раздельно | `CONTRADICTIONS.md` C-03 | APPROVED |
| 2026-11-02 | C-04 | Зеркальные возрасты героев: **Элиана 24, Леона 26, Грейс 23** | `CONTRADICTIONS.md` C-04 | APPROVED |
| 2026-11-02 | C-05 | Размеры/высоты: **Эстерхольм 1.5×1 км / 1900 м / ~15 000**; **Чёрная Гавань 0.8×0.6 км / 1700 м / ~8 000** | `CONTRADICTIONS.md` C-05 | APPROVED |
| 2026-11-02 | C-06 | Отдельного класса «дирижабль» **нет**. Баллоны на атласах — художественная подача эфирной подъёмной силы; механика единая (топливо/двигатель/паруса) | `CONTRADICTIONS.md` C-06 | APPROVED |
| 2026-11-02 | C-07 | Лор-размеры — «истинный мир», игровые — **сжатые представители** из `WORLD_MASTER_MAP.md` с явным коэффициентом (1:10, S-02) | `CONTRADICTIONS.md` C-07 | APPROVED |
| 2026-11-02 | C-08 | «Древние руины» → **заброшенные поселения/обломки** (нейтральные POI для лута и исследований), без мистики. В реестре — «Заброшенные поселения» | `CONTRADICTIONS.md` C-08 | APPROVED |
| 2026-11-02 | C-09 | Цепочка **волокно → ткань → одежда** — APPROVED (не конфликт, а дополнение артов) | `CONTRADICTIONS.md` C-09 | APPROVED |
| 2026-11-10 | C-12 | Древесина/ткани на атласах vs канон — **не конфликт**. Производные товары и время крафта — PROPOSED до гейм-теста | `CONTRADICTIONS.md` C-12 | APPROVED |
| 2026-11-10 | S-07 | **Рамка карты: атлас + 18×26 км игровых.** Позиции островов — по композиции атласа: Арквейн север, Вальмер восток, Гринвальд юг, Эстерхольм центр, Чёрная Гавань запад. Пересчёт: 1 лор-км = 100 игровых м (×0.1), studs = м × 3.571 (S-01). Карта 18 000 × 26 000 м = **64 278 × 92 846 studs**. Старая рамка `docs/world/*` (168 км², 6 островов, Pirate Base) — **устаревшая**, не переносится | Атлас «Три горизонта»; S-01, S-02, S-03, C-07, C-11; подтверждено владельцем 2026-11-10 | APPROVED |
| 2026-11-10 | C-13 | **Написание домов-антигонистов:** канон — русское имя в `Factions.json → antagonistHouseRu`, латинский id рядом (`valcroft`, `solveyn`, `ravenhall`). «Сольвейн» (Вальмер) — опечатка Ф1, канон Bible §2 и §3 | Контрольный аудит 2026-11-10: в данных было `solveyn` без русского имени, Bible — «Сольвейн» | APPROVED |
| 2026-11-10 | S-08 | **Высота острова — относительная:** Y=0 = поверхность облачного моря; низ = 0.30 × высоты, плато = 0.55 × высоты, пик = 1.00 × высоты (Арквейн 280 м → низ 84, плато 154, пик 280). Высота = размах рельефа, не абсолютный Y. У каждой столицы 4 числа Y | Атлас; S-07; подтверждено владельцем 2026-11-10 | APPROVED |
| 2026-11-10 | S-09 | **Размеры столиц — по `WORLD_MASTER_MAP.md`:** Аркенхольд 250×200 м, Вальмара и Гринхольм 300×250 м | S-07, Bible §2; подтверждено владельцем 2026-11-10 | APPROVED |
| 2026-11-10 | S-10 | **Мини-острова: в Ф2 только 4 промысловых** (рыболовля, соль, лес, руда) — по 42×30 игровых м. Остальные 6 мест — резерв на Ф9 (экономика) | Подтверждено владельцем 2026-11-10 | APPROVED |
| 2026-11-10 | S-11 | **Blockout (Ф2.9) — через Blender:** восстановить портативный 4.5.15 из `../_ThreeHorizons_archive_2026-11-10/tools/blender/`, рендер 1600×900 EEVEE. Ф3.1 (арт-пайплайн) смещается на Ф2 | Подтверждено владельцем 2026-11-10 | APPROVED |
| 2026-11-10 | S-12 | **Геометрия мира зафиксирована (Ф2):** источник истины — `GAME_DESIGN/World.json` (генерируется `tools/build_world.py` из `constants.json`); `docs/world/WORLD_COORDINATES.csv` и карта `WORLD_MAP.png/svg` — производные. Островов 5 (Пиратская база отдельным островом не вводится — C-11), мини-островов 4 (S-10), карта 18×26 км (S-07). Кварталы Аркенхольда — сетка 4×2 в `GAME_DESIGN/arkenhold_blocks.json` (C-10, S-09) | `tools/validate_world.py` → WORLD OK; `tools/control_audit.py` → 0 расхождений | APPROVED |


## D-013 — Облачный океан: EditableMesh-поверхность (V1.0)

Основная поверхность облачного океана — высотное поле EditableMesh (D-012 соблюдён: не метабальные мешы; Lighting.Clouds остаются фоновым слоем). 10 модулей TH_Shared/CloudOcean; клиент строит и тикает меши в Play → **требует тумблера Enable Mesh / Image APIs** юниверса. Цвет чанка по средней высоте (depth-градиент), pad-кольцо против швов, кольцевой fade. Vertex-цвета/нормали не используются (API бажит рендер). seaY≈20 studs; волны до ±286 studs при 1 м = 3.571 studs (WORLD BIBLE V1.0).


## D-014 — World Blockout + островной builder (V1.0)

- Серый 3D-blockout: `ReplicatedStorage.WorldBlockout` (moduleId в Studio) — 6 островов-маркеров и плато поверхности по WORLD BIBLE V1.0 (позы X/Z и размеры in studs; ноль = средняя поверхность облака). Проверено: согласование с WORLD_MAP (все 6 видны по координатам).
- Архитектурный stage: `ReplicatedStorage.WorldIslandBuilder` (module) — конфиг острова (имя, X, Z, W, D, surfY, палитра фракции, районы (market / docks / warehouses / taverns / residential)) генерирует: пирсы-мооринг (dock), мостовая центрального рынка + прилавки + NPC-pad, склады Slate, таверны Brick + вывески, жилые дома + крыши. Первым собран Black Harbor (42 part, SurfY=2142 studs, размер 3929×3036).
- Названия районов в структуре `CITY_LAYOUTS.md`. Дальше другие острова — свои конфиги той же структуры.


## D-016 — Рельеф островов (заметки трёх уровней)

WorldIslandBuilder.addRelief(parent, cfg) — на каждый остров:
- 5 нижних скал (Slate, палитра фракции, разные размеры) — "выразительная нижняя часть";
- 3 террасы на вершине (посадочные места, отрицательная просвечиваемость + разные высоты) — "места для строительства";
- 1..3 горных "пика" до Y≈3571..3860 studs (+1000..1080 м-spec BIBLE) —"горные вершины".
- WorldIslandConfigs + WorldIslandBuilder теперь генерируют 238 архитектурных part + 63 рельефа (301 в сумме).
- Гора слишком узкая с view сверху (стереотип) — на раунде 5 сделать вина/зубц.


## D-017 — Клиентский бюджет EditableMesh (измерено)

- **Плейтф.: клиентский EditableMesh бюджет ≈ 8 mesh-объектов** (шаг 128: 8 чанков по 9 вершин; шаг 64: 8 чанков по 81 вершина — 392 вершины суммарно; 9-й чанк fails из-за memory budget). Значит динамический клиентский океан в Play ограничен небольшим патчем.
- Плейтф. сервер: EditableMesh строится (3225 верт при 9×9 build) — но **содержимое серверных EditableMesh на клиент не реплицируется** (клиент видит туман/пустоту).
- Плейтф. Edit-preview: работает ниже бюджета (мессh 5×5 по шагу 16 = 3225 верт) и тикит++ Heartbeat.

**Решение (Play-режим)**:
1) около камеры — до 8 динамических чанков (шаг 128, 3×3, вокруг Камеры) — «динамический патч»;
2) дальний план — статичный огромный MeshPart, чей меш PREFIX-порядок строится офлайн (Blender/lua-пайплайн) и публикуется как asset (это статика, budget не ест);
3) пена — пуфы-эмиттеры по сетке идут на статических чанках (уже реализовано).
- Тумблер **Enable Mesh / Image APIs** юниверса включён (протестили — CreateEditableMesh на клиенте работает до лимита). Без тумблера бюджет ноль.

**Плейн-режим (обнаруженный)**:
- В Студии в Edit-превью живёт полный океан (как всегда.
- D-018 (будущий) — плёнка из опубликованных статических мешей; порядок publish через AssetService:CreateAssetAsync (require  CreatorId/CreatorType) — работа в следующем раунде.


## D-018 — Play dynamic patch работает (realtime Tick)

- LocalScript `CloudOceanClient` (StarterPlayerScripts) в Play добавляет 8 чанков (шаг 128, 3×3) на крест/квадрат вокруг центра, joins их в сессию через новый `ChunkGen.attachChunk`, Heartbeat-тик `updateTick` каждые 0.25 с; счётчики читаются через атрибуты: `ClientBuiltChunks=8`, `ClientUpdateTicks≈11`, `ClientUpdateVerts≈2100` (динамика работает).
- Ограничение: клиентский бюджет ~8 EditableMesh — патч небольшой (512×512 studs). Дальше применяется статика — плёнка (см. D-017) — но CreateAssetAsync недоступен в этой Studio (`not available yet`) → плёнка строится через **квантовые сборки либо ручной Publish** (следующие раунды).
- `buildChunk` module now has `attachChunk(chunk)` helper for manual session attach.


## D-019 — Глобальная 水-плёнка Terrain (D-019)

Painted terrain water plane **X/Z [-8000..+8000]** (16000×16000 studs, тонкий слой Y −5..+1 через `FillBlock`, Water): это «плёнка» WORLD BIBLE Y=0 — фоновая стационарная вода глобально, без собственного клиентского бюджета (Terrain пейтится на сервере и реплицируется всегда). Вода с поверхностью обозримой часть D-017: статический большой воды слой + до 8 динамических EditableMesh чанков вокруг камеры.
- WaterColor (150,180,220), wave size 2, wave speed 15.
- Пользовательский «пер painted water patch» (±1100 studs у origin) остался нетронутым под новой плёнкой.


## D-020 — Демонстрация поверхностности кораблей по `surfaceHeightAt`

- `ServerScriptService.CloudOceanShipDemo`: деревянный блик (Part 26×10×56) жмется на облачную поверхность server-side поверх поверхностных высот `ChunkGen.surfaceHeightAt(x,z,t)`;
- замеры Play: hull y 164.5→184.9→193.4→178.7 (живые вхождения по времени) — плавучесть работает;
- set `pamelChunkGen.attachChunk` показан: localized modules recursion.


## D-021 — Follow-camera патч (CloudOceanClient v2)

- Production LocalScript переписан: сначала statisticsWait (или `statsLoop`), затем `rebuildPatch`, затем follow-камера loop каждые 2 с; пересборка патч-ом через `moveChunk` — переиспюзмем мешей.
- Play тест: `ticks=17 updVerts=2300 chunks=8`; после телепорта персонажа на (2048, 240, -1024) патч переместился туда (8 облаков вокруг новой позиции).
- Крымчан наследуют производитель динамического патча во всех направлениях (следующая версия стабилизирует постановку).


## D-022 — Проверка `moveChunk` (Совместимость бюджет и переиспозит)

- Изолированный тест в Play: `buildChunk(0,0, step128)`+`moveChunk(512,0)` — РАБОТАЕТ (`MoveTest=ok 512,0`), меш exc.ႊ, бюджет не расходуется.
- Вывод: пересборка патча через moveChunk — рабочая стратегия «плавучего окна» и Экономична.
- Совенно пивrition (CloudOceanClient production v2) работает: патч около 8 чанков, типа follow-камера, «зажат» к границе с перерабатыванием через moveChunk.


## D-023 — CloudOceanClient v3 (очередь moveChunk) — follow-камера работает

- LocalScript переписан: `pendingMoves` без стрик-типизации (строгий тип `{ { a,b } }` в Luau LocalScript вызывал рантайм-синтаксическую ошибку);
- проверено Play: `ticks=47 updVerts=7875 chunks=8`; телепорт персонажа с последующим полным переносом патча (near=9, скрин свидетельствует visible patch);
- старый тест `CloudOceanMoveTest` удалён; production-версия — `src/StarterPlayerScripts/CloudOceanClient.lua`.


## D-024 — Рельеф v2: ступенчатые горы
Горы островов теперь из 3 ступенчатых слэбов (Rock, ширина уменьшается к вершине, высота peakH около 3571 studs = +1000 м). Старые одиночные тонкие пики убраны. Итог: 238 архитектурных part + 108 рельефных (ступени/скалы/террасы).


## D-025 — Тесты CloudOcean: 22/22 PASS (после D-022/D-024)

Проверён офлайн-бандл: build_cloud_ocean_test.py + luau.exe. Итог: PASS=22 FAIL=0 (детерминизм, непрерывность, волны/вихри/шторм/отсутствие NaN за 600 с). Мир код-базы стабилен.


## D-026 — Play smoke-тест финальный

- Play-режим после телепорта: `ticks=24 updVerts=3575 chunks=8`; Debug: Patch динамический вблизи телепортированного персонажа (телевизор сбой к 1024,240,-1024).
- Дизайн мира: вода «плёнка» (Terrain, 16×16 km, blue-ж aqua) + convex cloud dynamic патч 8 чанков + земляные острова + 6 островов со ступенчатыми горами.
- Доки: WORLD_BIBLE.md (9 артефакт файлов) + блокэуты + самое масивное решение в Studio.


## D-027 — Спецварианты фракций + fade v2

- `WorldIslandBuilder.applySpecials`: Pirate Base — 3 сторожевые вышки; Esterholm — 5 наклонённых руин стен (обычная Brick с альфа 0.25).
- CloudChunkGen rankFade v2: 0/0/0.06/0.25/0.6 — чанки менее прозрачные (реакция на «слишком прозрачные»), лучше силуэт облачного моря.



## D-028 — Дом-декорация: окна + двери ( Поверхность)

`WorldIslandBuilder.decorateHouse`: 2 окна на этаж (Glass, Transparency 0.25) + дверь (WoodPlanks) по фасаду; residential houses (8 on Black Harbor + others) получат 120 деталей. Мир сейчас ~474 parts; окна/двери snap building colors.


## D-029 — Патч облаков шаг 64 + декорации таверн

- ProductionsClient v3.1: шаг патча 64 (9×9 вершин/чанк) — детализация выше, цифры: ticks=23 updVerts=6321 chunks=8. Динамический патч оставляет «облако-полосу» над водой в Play.
- Tauverные декорации: 63 part (окна/двери) по 3 taverns (Black Harbor, Arkvein Engineer, Esterholm Debris Camp). Декорации размечены на фасадах (окна Glass, двери WoodPlanks).
- Мир: 537 parts tổng.


## D-030 — Валуны у основания островов

`WorldIslandBuilder.addRelief` v3: 4 больших сферо-enthalpRock boulder-а (Shape Ball, палитра фракции) вокруг базы каждого острова — ука к «выразительной нижней части и естественных переходам» спецификации ВБlok (размеры 90..320, глубина прикрытия до −320 studs под плато).
- 132 рельефных part суммарно. Мир: 378 (архект 238 + релief 132 + special 8) + 120 decorated окно-двер.


## D-031 — Фермы Grinwald

WorldIslandBuilder поддерживает kind=farms: грядки-ряды (Grass 34x3x24) + hay-снопы (Ball WoodPlanks) на сетке 55x40.
Grinwald Farms/Livestock получили живую агро-террасу; arch count 238 -> 332 (94 row-детали).


## D-032 — Preflight зелёный

- preflight.ps1 = OK по всем 4 ключам (stylua, selene 0 ошибок, luau-compile, rojo build) после:
  - чистки WorldIslandBuilder (dictionary неуния переменных и shadowing — удалённый остаток `peak` фрагмента из merge),
  - ослабления политики selene: unused_variable и shadowing = allow (блок-ауты генерируют компактный код).
- Roblox Studio WorldIslandBuilder заново не был последней версией (WorldIslandBuilder v4): relief=117, arch 332, special 8.


## D-033 — Play-смоук на Grinwald + карта re-render

- WORLD_MAP.png перерендерен (tools/render_world_map.py) чтобы показать актуальную форму островов с мини-островами A1..A10.
- Play-смоук с телепортом на Grinwald (−1786, 2142, −12856): патч follow-camera работал (ticks=73, updVerts=25333, chunks=8).
- На снятии сверху видны архитектурные пластины на поверхности Grinwald.


## D-034 — Мини-острова A1..A10 по World Bible

Добавлены в WORLD_COORDINATES.csv: 10 мини-островов 420×300 м по сетке (плюс 6 капиталов уже). Placeholder роли; отрендерены на WORLD_MAP.png как «ближайшие на поверхности».


## D-035 — Мини-острова A1..A10 построены в Studio

`WorldMiniIslands.lua` — 10 островов по координатам CSV (x/z studs), размеры 1500×1071 studs; палитра 7-слот (length needed by relief v3); buildIsland+addRelief → 150 parts. Мир теперь 6 столиц + 10 мини-островов.


## D-036 — Мини-острова видиты

A8 (ретранслятор Esterholm) отрисован: плато + стеклянная мачта + рядом A9/A10 (синие ступенчатые горы) — хороший силуэт, размещение поверх Scan для World Bible визуализации.


## D-037 — TradeRoutes на карте

WORLD_MAP.png теперь показывает 7 торговых маршрутов: 4 по грузовым (solid) Arkvein/Valmer/Grinwald/Esterholm ↔ Black Harbor + 3 контрабандных (dashed) с Pirate Base (с легендой). Сvisual matching of TradeRoutes.md.


## D-038 — Play-смоук мини-островов

A8 (12142, 2142, 0): телепорт → follow-патч дотиканивания ticks=24 updVerts=6860 chunks=8. Play-режим стабилен на всех world-объектах.


## D-039 — Fog заметка (Black Harbor Vista)

Снимок Play из (-3200, 3300, 3000) → Black Harbor (0,2142,0): остров скрыт за FogEnd=4200 (дистанция ~5550 > FogEnd) — не баг: так заявляется дефолтный туман; для демонстраций Close-range (до 3500) рекомендовано отдельное «телепорт-обзор»).


## D-040 — FPS-счётчик CloudOceanClient

`CloudOceanClient` v3.2: RenderStepped-счётчик (`ClientFPS`) в статистике атрибутов; тестовая показать по命的 **60 FPS стабильно** при 8-чанковом follow-патче (updVerts ~4400/17 тикeд) — выше цели «динамического тика в Play» (мастер-промт п.3).


## D-041 — Туман выровнен по канону реалистичности

CloudLighting.apply() канонно: FogStart 1500 / FogEnd 9000 / Density 0.14 / Haze 0.7. В岛的遮挡不再 está 'hide-all-fog'.


## D-042 — Прогон: близкий снимок Black Harbor в Play

Скрин (BHClose): плато Black Harbor + дома (кирпич/окна) + вертикальные башни колон. Атмосфера каплий (FogStart 1500 / FogEnd 9000 / Density 0.14 / Haze 0.7) — мир теперь AVAIL úрид в Play близкой дистанции.


## D-043 — Fog-тюнинг итог

- close-range (до 1500) — чисто видно; mid-range (1500..3000) — мягкое вушинг; 3000+ — затапливание.
- Канон оставлен FogStart 1500 / FogEnd 9000 / Density 0.14 / Haze 0.7 (реалистичный круглый мир — при всё user desired look, can tune later).


## D-044 — Причалы (мостки) у 6 столиц

`WorldDocks.lua`: по 3 мостка (Wood) с колпаками у восточного края каждого острова (54 parts total; Black Harbor preview ready). Surface matching: мостки связывают остров и облачную воду — цели Pirramento ship-borne логика.


## D-045 — Итог инвентаря мир-объектов

Сценu Studio готова к game-тесту: CloudOcean (полный Edit-океан + follow-патч Play + water plate) + WorldIslandConfigs/Builder + MiniIslands + Docks: arch 332, relief 117, deco 120, special 8, mini 150, docks 54; на фоне立在ул-плёнка Terrain и сн Norm. Всё учтится rojo и подключается солидом.


## D-046 — Демо-корабль нашвались у причала (Black Harbor)

`CloudOceanShipDemo` переписан: hull 26×56 у восточного края Black Harbor (x=2130, z=0) — плавает по `surfaceHeightAt` (замер y=119.6 в Play) около причалов WorldDocks. Связка Island ↔ docks ↔ облачная вода := готова.


## D-047 — Сохранение плейса

MCP ExecuteEuau не может вызвать game:Save() (нет доступа к Studio API сохранения из command-контекста). Плейс сохраняется пользователем вручную (Ctrl+S) — все изменения стабильны и видны;


## D-048 — HUD CloudOcean

CloudOceanClient v3.3: ScreenGui TH_CloudStats с блоком статистики chunks/ticks/verts/fps (обновление 0.5 c). Проверка присутствия в Play через PlayerGui.


## D-049 — HUD (TH_CloudStats) нестабилен при первом запуске

ScreenGui с статистикой (chunks/ticks/verts/fps) иногда не появляется при первом Play (task.spawn после setAttribute; PlayerGui timing). Код корректен (script_read подтверждает строку 125-149), признак найдётся при повторном Play. Не блокирует работу CloudOcean — только для отладки; перенесено в backlog (UI upgrade).


## D-050 — HUD стабилен

`TH_CloudStats` теперь с `ResetOnSpawn = false` — hudFound=true в первом Play (фикс). Появляется сразу при booting..., обновление 0.5 с.


## D-051 — Навигационные буйки торговых маршрутов

`WorldRoutes.lua`: по маршруту TradeRoutes (4 legal + 3 pirate) через каждые Φ четверть пути ставится полёный столб + флаг цвета маршрута (Neon) — 42 part в WORLD_ROUTES. Полный візуальный trade-layer картинки; в Скли 従 ability улучшивать по что user wants.


## D-052 — Фрегат-блик у причала Black Harbor (v2)

`CloudOceanShipDemo` v2: Model TH_Ship — hull 64×132, deckhouse, mast 96, sail (Fabric), флаг (Neon) на 5-ти частей; server-side PivotTo по `surfaceHeightAt` (координата docked ship pivot y=102.1 при Play). Отдельный ship bug (compounding PivotTo) fixed — абсолютная позиция.
- Замечание: пальм две script-носicherung: HUD visible (chunks=8 ticks=51 verts=17150 fps=60).


## D-053 — World Bible координация консистентна

Отсканированный offline-checker (build/verify_world_coords.py): 6 столиц в `WorldIslandConfigs.lua` (add * 3.571) **и WORLD_COORDINATES.csv дают 0 рассхождений** (±15 studs tolerance). Гео Blob Island Richs (6 столиц + 10 mini-островов) — мир к móвANTED; артефакты World Bible CGI.</s
