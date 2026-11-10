# КАРТА АРТЕФАКТОВ — кто создаёт, кто читает

> Связи между фазами. Читать, когда: добавляете новый артефакт, меняете формат существующего
> или ищете, кто зависит от вашего файла.

> Обновление: после каждой фазы, где появился новый артефакт.

| Артефакт | Создаёт | Читают |
|---|---|---|
| `ARCHITECTURE.md` | Ф00 · 0.1 | Ф00, Ф01, Ф08, Ф09, Ф16 |
| `Buildings.json` | Ф06 · 6.8 | Ф04, Ф07, Ф20 |
| `CHANGELOG.md` | Ф00 · 0.7 | Ф00 |
| `CITY_LAYOUTS.md` | Ф09 · 9.1 | Ф01 |
| `CONTRADICTIONS.md` | Ф02 · 2.10 | Ф01, Ф02, Ф03 |
| `Config/Bundle.lua` | Ф01 · 1.13 | Ф08 |
| `DECISIONS.md` | Ф00 · 0.7 | Ф00, Ф02, Ф19 |
| `DESIGN_TOKENS.md` | Ф03 · 3.2 | Ф01, Ф03, Ф06, Ф07, Ф09, Ф16 |
| `Factions.json` | Ф21 · 21.5 | Ф16, Ф19, Ф21 |
| `GAME_DESIGN/Style.json` | Ф03 · 3.1 | Ф03 |
| `Goods.json` | Ф10 · 10.4 | Ф16, Ф19, Ф20, Ф21 |
| `MASTER_SCALE_SPEC.md` | Ф04 · 4.2 | Ф01, Ф02, Ф04, Ф07, Ф09 |
| `Main.server.lua` | Ф08 · 8.7 | Ф00 |
| `Professions.json` | Ф16 · 16.9 | Ф21 |
| `README.md` | Ф00 · 0.1 | Ф22 |
| `ROADMAP_0.2.md` | Ф13 · 13.9 | Ф22 |
| `STATUS.md` | Ф08 · 8.12 | Ф00, Ф09, Ф10, Ф12, Ф14, Ф15, Ф17, Ф18, Ф22 |
| `Ships.json` | Ф10 · 10.4 | Ф10 |
| `Strings.json` | Ф17 · 17.2 | Ф17 |
| `Style.json` | Ф03 · 3.2 | Ф03 |
| `WORLD_COORDINATES.csv` | Ф02 · 2.2 | Ф02, Ф14 |
| `Weather.json` | Ф12 · 12.9 | Ф10, Ф18 |
| `arkenhold_blocks.json` | Ф02 · 2.9 | Ф02, Ф21 |
| `blender/visual_library.json` | Ф04 · 4.1 | Ф04 |
| `docs/DECISIONS.md` | Ф00 · 0.11 | Ф04, Ф12 |
| `docs/NAMING.md` | Ф00 · 0.8 | Ф17 |
| `docs/STATUS.md` | Ф00 · 0.7 | Ф16 |
| `docs/story/PLOT.md` | Ф19 · 19.1 | Ф19 |
| `export_config.py` | Ф05 · 5.3 | Ф05 |
| `tools/TOOLCHAIN.md` | Ф00 · 0.4 | Ф00 |
| `tools/preflight.ps1` | Ф05 · 5.11 | Ф00 |
| `tools/test.ps1` | Ф08 · 8.10 | Ф01, Ф08, Ф10, Ф12, Ф16 |
| `tools/validate_world.py` | Ф02 · 2.6 | Ф09 |
| `travel_times.json` | Ф10 · 10.10 | Ф02 |
| `validate_assets.py` | Ф05 · 5.11 | Ф05 |
| `validation.json` | Ф05 · 5.5 | Ф07 |
| `world/ISLAND_CATALOG.md` | Ф02 · 2.2 | Ф02, Ф09 |

## Создаются и больше не читаются другими фазами

| Артефакт | Создаёт |
|---|---|
| `AUDIO_DESIGN_BIBLE.md` | Ф14 · 14.11 |
| `Audit.lua` | Ф08 · 8.9 |
| `BUILDING_CATALOG.md` | Ф04 · 4.6 |
| `ClientMain.client.lua` | Ф08 · 8.7 |
| `Config/Clouds.lua` | Ф12 · 12.3 |
| `Config/Factions.lua` | Ф08 · 8.5 |
| `GAME_DESIGN/Combat.json` | Ф13 · 13.1 |
| `GAME_DESIGN/Fleet.json` | Ф18 · 18.1 |
| `GAME_DESIGN/Settlements.json` | Ф20 · 20.1 |
| `GAME_DESIGN/Strings.json` | Ф17 · 17.1 |
| `GAME_DESIGN/arkenhold_blocks.json` | Ф02 · 2.8 |
| `GAME_DESIGN/constants.json` | Ф02 · 2.1 |
| `Goods.lua` | Ф08 · 8.5 |
| `MeshAssets.lua` | Ф05 · 5.10 |
| `Migrations.lua` | Ф08 · 8.8 |
| `Palettes.lua` | Ф08 · 8.5 |
| `PascalCase.lua` | Ф00 · 0.8 |
| `PlayerData.lua` | Ф08 · 8.8 |
| `Prices.json` | Ф13 · 13.1 |
| `RELEASE_CHECKLIST_ALPHA.md` | Ф22 · 22.1 |
| `ROADMAP_0.1.md` | Ф00 · 0.11 |
| `ROBLOX_IMPLEMENTATION/build/TH_base.rbxlx` | Ф00 · 0.12 |
| `ROBLOX_IMPLEMENTATION/default.project.json` | Ф08 · 8.1 |
| `RateLimit.lua` | Ф08 · 8.9 |
| `SeededRNG.lua` | Ф08 · 8.4 |
| `Ships.lua` | Ф08 · 8.5 |
| `Signal.lua` | Ф08 · 8.4 |
| `TH_Client/UI/Kit.lua` | Ф14 · 14.1 |
| `TH_Server/Ships/CombatService.lua` | Ф13 · 13.2 |
| `TH_Server/Ships/FleetOffline.lua` | Ф18 · 18.2 |
| `TH_Server/World/WorldEvents.lua` | Ф18 · 18.5 |
| `TableUtil.lua` | Ф08 · 8.4 |
| `TimeUtil.lua` | Ф08 · 8.4 |
| `Types.lua` | Ф08 · 8.3 |
| `Validators.lua` | Ф08 · 8.9 |
| `Wallet.lua` | Ф08 · 8.9 |
| `Weather.lua` | Ф08 · 8.5 |
| `Window.lua` | Ф14 · 14.2 |
| `WorldAssembler.lua` | Ф09 · 9.3 |
| `blender/README.md` | Ф05 · 5.2 |
| `blender/manifest.json` | Ф05 · 5.7 |
| `blender/presets/export_preset.md` | Ф05 · 5.3 |
| `blender/renders/studio.blend` | Ф04 · 4.2 |
| `blender/sounds/manifest.json` | Ф15 · 15.1 |
| `blender/textures/manifest.json` | Ф06 · 6.1 |
| `build/TH_dev.rbxlx` | Ф08 · 8.11 |
| `default.project.json` | Ф00 · 0.12 |
| `docs/ASSET_REGISTRY.md` | Ф07 · 7.1 |
| `docs/PROJECT_STATUS.md` | Ф00 · 0.7 |
| `docs/SESSION_TEMPLATE.md` | Ф00 · 0.10 |
| `docs/STYLE_BIBLE.md` | Ф03 · 3.8 |
| `preflight.ps1` | Ф08 · 8.11 |
| `tests/run.lua` | Ф08 · 8.10 |
| `tools/backup.ps1` | Ф00 · 0.9 |
| `tools/blender.ps1` | Ф05 · 5.1 |
| `tools/bump_version.py` | Ф00 · 0.9 |
| `tools/bundle_design.py` | Ф01 · 1.13 |
| `tools/gen_textures.py` | Ф05 · 5.8 |
| `tools/make_cloud_puff_textures.py` | Ф12 · 12.4 |
| `version.json` | Ф00 · 0.9 |
| `visual_library.json` | Ф04 · 4.3 |

## Ключевые цепочки данных

Главный поток: **канон → данные → бандл → код → ассеты → мир → геймплей**.

```
docs/*.md (канон)
   ↓ Ф1  перевод канона в данные
GAME_DESIGN/*.json
   ↓ Ф1.13  bundle_design.py
GAME_DESIGN/bundle.json + Config/Bundle.lua
   ↓ Ф8  Roblox-каркас читает Bundle
Luau-модули
   ↓ Ф7  ассеты + Ф9  мир
игра
```

Поток стиля: **Ф3 Style.json → Ф4 рендеры → Ф5 пайплайн → Ф6 текстуры → Ф7 ассеты**.
Поток мира: **Ф2 координаты → Ф9 квартал → Ф10 корабль → Ф11 интерьеры → Ф13 бой**.
Поток содержания: **Ф16 механики → Ф19 сюжет → Ф21 фракции**.
Поток звука и UI: **Ф14 UI/звук → Ф15 звуковая библиотека → Ф17 локализация**.
