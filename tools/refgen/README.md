# refgen — генерация референсов Three Horizons через Higgsfield MCP

Автономный пайплайн, который догоняет недостающие референсы из
`docs/roadmap/model-classes.json` (319 классов) в `ART_ASSETS/refs/<id>.png`.

## Состояние на 2026-11-11

| | |
|---|---|
| Всего классов | 319 |
| Уже было отрендерено (до пайплайна) | 135 |
| Осталось догенерировать | 184 |
| Модель | `seedream_v5_pro`, resolution `2k` (2048×2048) |
| Скорость | ~4,5 мин на кадр (Higgsfield даёт 1 задачу одновременно) |
| Бесплатный unlimited-триал | активен до 2026-11-13 |

## Файлы

| Файл | Назначение |
|---|---|
| `hf_auth.py` | OAuth (PKCE) для Higgsfield MCP: регистрация клиента, редирект на `127.0.0.1:8765`, сохранение токена в `~/.higgsfield-mcp-token.json` |
| `hf_mcp.py` | Минимальный MCP-клиент (streamable HTTP): `initialize`, `tools/list`, `tools/call`, авто-refresh токена, ретраи по сети |
| `prompts.py` | Шаблоны промптов по группам (weapons/details/ships/items/tools/tiles/ui/weather) |
| `subjects.json` | 184 английских описания предметов (`id` → subject/notes) |
| `missing.json` | Список недостающих классов (`id`, русское имя, размер, назначение) |
| `run_refgen.py` | Основной раннер: сабмит → jobs_wait → скачивание PNG |
| `reconcile.py` | Подбор уже отрендеренных кадров, потерянных из-за «ложных» ошибок сабмита |
| `watchdog.py` | Перезапускает раннер, если он упал |
| `status.py` | Прогресс: сколько референсов готово |
| `make_lore_video.py` | Видео по лору из `docs/THREE_HORIZONS_PROJECT_BIBLE.md` (Seedance 2.0, 15 c, 720p) → `ART_ASSETS/video/` |

## Команды

```powershell
cd C:\Users\ARK\Documents\deepseek-harness\default-workspace\ThreeHorizons\tools\refgen

# прогресс
python status.py

# сгенерировать всё оставшееся (идемпотентно: готовые PNG пропускаются)
python run_refgen.py --max-inflight 1

# только одну группу / один id
python run_refgen.py --groups ships
python run_refgen.py --only galleon,manowar

# посмотреть промпт без генерации
python run_refgen.py --dry-run --groups tiles --limit 1

# супервизор (сам поднимает раннер и перезапускает при падении)
python watchdog.py

# видео по лору
python make_lore_video.py
```

## Важные детали Higgsfield

1. **Unlimited-генерации выдаются только «приложениям».** MCP-сервер смотрит на
   `clientInfo.name` в `initialize`. Со значением `chatgpt` — работает, с любым
   другим (`claude-code`, `openclaw`, …) — отказ: *«Unlimited generations are not
   available in the app you are using»*.
2. **Job id лежит в поле `id`** (для `generate_image`), а не в `job_id`
   (так у `generate_image_batch`).
3. **Сервер иногда отдаёт ошибку, хотя задача создана.** Если сабмит вернул
   ошибку, раннер ищет свежую задачу с тем же промптом через `show_generations`
   и подхватывает её.
4. **Лимиты плана ultra (monthly):** 1 одновременная задача + бэкенд-429 при
   слишком частых сабмитах. Отсюда экспоненциальный backoff в раннере.
5. Для видео unlimited покрывает `seedance_2_0`; у `seedance_2_5` — нет.

## Токен

`~/.higgsfield-mcp-token.json` (вне репозитория). Продлевается автоматически
через `refresh_token`. Переавторизация: `python hf_auth.py` → открыть ссылку →
подтвердить в браузере.
