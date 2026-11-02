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
