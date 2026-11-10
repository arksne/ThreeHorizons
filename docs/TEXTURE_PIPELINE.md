# TEXTURE PIPELINE (v1.1, APPROVED)

## Что сгенерировано
22 материала × 3 карты (`_a` albedo, `_n` normal, `_r` roughness), 512×512, палитры строго из `DESIGN_TOKENS.md`.

Материалы по фракциям:
- **Арквейн:** ARK_Stone, ARK_Cobble, ARK_WoodDark, ARK_Slate, ARK_Copper, ARK_Steel
- **Вальмер:** VAL_Limestone, VAL_Cream, VAL_Sand, VAL_SeaSlate, VAL_Bronze, VAL_WhiteMarble, VAL_TealCanvas
- **Гринвальд:** GRN_Plaster, GRN_Wood, GRN_Terracotta, GRN_StrawThatch, GRN_Stone, GRN_OliveCanvas
- **Общие:** NET_SailCanvas, NET_ShipHull, NET_DarkWoodUI

Проверено визуально (скрин-контроль в сессии): камень/кирпич/известняк/сланец/медь/парусина/солома — читаемая фактура; мрамор — прожилки; normal-карта камня корректно даёт рельеф кладки.

## Шаг 1. Загрузка в Roblox
1. Creator Dashboard → Creations → ваш Place → **Asset Manager** → Upload → Images.
2. Загрузить 66 PNG (можно папкой). Имена не менять — по ним работает `MaterialConfig`.
3. Записать asset id каждого файла.

## Шаг 2. Прописать ID
В `ReplicatedStorage/TH_Shared/Config/MaterialConfig.lua` (создаётся в Ф6 (текстуры)) заполнить таблицу:
```lua
MaterialConfig.TEXTURE_IDS.ARK_Stone = {
    albedo    = "rbxassetid://0000000001",
    normal    = "rbxassetid://0000000002",
    roughness = "rbxassetid://0000000003",
}
```
Или через код: `MaterialConfig.setFor("ARK_Stone", albedo, normal, roughness)`.

## Шаг 3. Где применяется
- `Builder.build` (сервер/Studio) — после создания Part вызывает `MaterialConfig.apply(part, token)`.
- Если ID не заданы — фолбэк: `Color3` палитры + стандартный `Material` (как в v1.0), ничего не ломается.

## Правила (худконтроль A-1)
- Тайлинг: `SurfaceAppearance.TileSize = 4` (4 м на тайл). Не менять без записи в DECISIONS.
- Текстуры бесшовные: тайлинг по X/Z не должен давать швов (проверять на стене 12×8 м).
- Normal не «пережимать»: strength задан уровнем 2.4 в генераторе.
- Один материал = один набор из 3 карт. Дубликаты не создавать — сверяться с `ASSET_REGISTRY.md`.

## Ограничения
- Лимит Roblox на загрузку изображений зависит от аккаунта/подписки — 66 файлов может потребовать нескольких сессий загрузки.
- Внутри Studio текстуры появятся только после модерации ассетов.
- PBR-качество: Roblox SurfaceAppearance поддерживает ColorMap/NormalMap/RoughnessMap/MetalnessMap; Metalness в текущих текстурах не задаётся (только roughness).
