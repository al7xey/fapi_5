# Контрольная работа №5

Проект на FastAPI для управления задачами, работы с WebSocket-комнатами,
внедрения зависимостей, проверки прав доступа и интеграционного тестирования.

## Структура проекта

- `app/main.py` — создание FastAPI-приложения и подключение роутеров.
- `app/routers/` — маршруты для задач, пользователей, администратора и комнат.
- `app/dependencies.py` — зависимости для авторизации и проверки роли администратора.
- `app/storage.py` — in-memory хранилище задач.
- `app/room_manager.py` — менеджер WebSocket-комнат.
- `tests/` — интеграционные тесты HTTP-эндпоинтов и WebSocket.

## Локальный запуск

```bash
python -m venv .venv
```

```bash
pip install -r requirements.txt
```

```bash
uvicorn app.main:app --reload
```

API будет доступно по адресу `http://localhost:8000`.

## Запуск тестов

```bash
pytest
```

## Запуск через Docker

```bash
docker compose up --build
```

Проверка эндпоинта задач:

```bash
curl http://localhost:8000/tasks -H "X-User-Id: 10"
```

Ожидаемый ответ для пустого списка задач:

```json
[]
```

Проверка состояния приложения:

```bash
curl http://localhost:8000/health
```

При запуске через Docker ответ будет таким:

```json
{
  "status": "ok",
  "env": "docker"
}
```

## Основные эндпоинты

- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}/status`
- `DELETE /tasks/{task_id}`
- `GET /users/me`
- `GET /users/{user_id}`
- `GET /admin/stats`
- `DELETE /admin/tasks/{task_id}`
- `GET /rooms/{room_id}/users`
- `WebSocket /ws/rooms/{room_id}?username=alice`

## Авторизация

Для HTTP-эндпоинтов используется заголовок:

```http
X-User-Id: 10
```

Для административных маршрутов дополнительно нужна роль:

```http
X-User-Role: admin
```
