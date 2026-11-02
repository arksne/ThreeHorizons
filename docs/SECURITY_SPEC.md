# SECURITY SPEC (APPROVED v0.1)
> Отдельный документ (ядро было в SPECS_COMBINED, здесь — полная версия).

## Принципы
1. Сервер — единственный авторитет: деньги, грузы, владение, награды, урон, сохранения.
2. Клиент шлёт только намерения через NetAPI v1 с txId; повтор txId = no-op.
3. Прайс только серверный (Goods.lua); клиентские цены игнорируются.
4. Весь текст другим игрокам — через TextService:FilterStringAsync.

## Проверки Validators.lua
Тип, диапазон, владение объектом, кулдаун, дистанция <40 st, состояние (не мёртв/не в бою для торговли).

## RateLimit (сервер, жёстко)
interact 10/с, trade 5/с, ship/crew 5/с, property 3/с, chat 3/с. Превышение: warn → kick → бан-таблица (MemoryStore).

## Аудит
Audit.lua: все перемещения strategic goods сверх порога (топливо/кристалл/зерно ≥50), все захваты кораблей, все покупки property. Формат: {t, userId, action, item, qty, txId}.

## DataStore
Только UpdateAsync из сервера; BindToClose очередь; бэкап corrupt-профилей `_corrupt_<time>`.
