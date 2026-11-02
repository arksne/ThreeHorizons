# QUALITY ASSURANCE (APPROVED v0.1)

## Gate A-1 — худконтроль (каждый ассет final/lod)
- [ ] Масштаб по MASTER_SCALE_SPEC (дверь 1.0×2.1, pivot в основании, фасад +Z)
- [ ] Токены только из DESIGN_TOKENS (magenta = провал)
- [ ] Имя TH_* по ASSET_REGISTRY, без дублей (grep)
- [ ] LOD: L0 полный + L1 без декора (>300 st) для final
- [ ] Коллизии: CanCollide только корпус/пол; декор — false
- [ ] Бюджет: дом ≤60 боксов L0

## Gate S-1 — система (каждый серверный модуль)
- [ ] Юнит-тест в tests/ проходит
- [ ] Плей-тест: сервер + 2 клиента, Output без ошибок
- [ ] Remote ≤60/с/игрок, нет прямых Set из клиента
- [ ] Сохранение переживает leave/rejoin (ручной тест)

## Gate R-1 — релиз этапа
Все gates + CHANGELOG + бэкап в backups/ + запись DECISIONS при смене лора.

## Статус ассета
concept (арт) → blockout (боксы) → final (материалы/UV) → lod (уровни). Концепт моделью не считается.
