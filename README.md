# FastAPI Control Work 5

FastAPI application for task management, WebSocket rooms, dependency injection,
and integration testing.

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
