# FastAPI Control Work 5

FastAPI application for task management, WebSocket rooms, dependency injection,
and integration testing.

## Project Structure

- `app/main.py` creates the FastAPI application.
- `app/routers/` contains task, user, admin, and room routes.
- `app/dependencies.py` contains authentication and authorization dependencies.
- `app/storage.py` contains the in-memory task storage.
- `tests/` contains integration tests for HTTP routes and WebSocket behavior.

## Local Run

```bash
python -m venv .venv
```

```bash
pip install -r requirements.txt
```

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Tests

```bash
pytest
```

## Docker

```bash
docker compose up --build
```

Check the tasks endpoint:

```bash
curl http://localhost:8000/tasks -H "X-User-Id: 10"
```

Expected response for an empty task list:

```json
[]
```

Check service health:

```bash
curl http://localhost:8000/health
```

## Main Endpoints

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
