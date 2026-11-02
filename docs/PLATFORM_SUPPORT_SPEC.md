# PLATFORM SUPPORT SPEC (APPROVED v0.1)

## Устройства
- Windows / macOS: полный профиль (тени вкл, TargetRadius 1200 st, дальние LOD).
- Mobile / планшет: TargetRadius 500 st, тени выкл, LOD−1, текст ≥14px, кнопки ≥44pt.

## Управление (едино с UX_DESIGN_SPEC)
E — действие, F — якорь, M — карта, Tab — инвентарь. На тач — те же глаголы кнопками, штурвал — виртуальный джойстик + слайдер газа/высоты.

## Графпрофили
Low / Med / High + Auto (FPS<30 дольше 5 с → шаг вниз). Настройки хранятся в профиле (Settings в mapFog-слоте нет — отдельный ключ settings).

## Тесты устройств
Каждая сцена гоняется на Low (потолок бюджетов из OPTIMIZATION_PLAN): ≤8000 near-parts, ≤25 NPC рядом, свет 1 Directional.
