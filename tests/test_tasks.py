import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import task_storage


@pytest.fixture(autouse=True)
def clean_storage():
    task_storage.reset()
    yield
    task_storage.reset()


@pytest.fixture
def client():
    return TestClient(app)


def make_task(client, user_id="10", **overrides):
    payload = {
        "title": "Prepare tests",
        "description": "Write integration tests",
        "status": "todo",
        "priority": 4,
    }
    payload.update(overrides)
    return client.post("/tasks", json=payload, headers={"X-User-Id": user_id})


def test_create_task_success(client):
    response = make_task(client)

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Prepare tests",
        "description": "Write integration tests",
        "status": "todo",
        "priority": 4,
        "owner_id": 10,
    }


def test_short_title_returns_422(client):
    response = make_task(client, title="Hi")

    assert response.status_code == 422


def test_missing_user_header_returns_401(client):
    response = client.get("/tasks")

    assert response.status_code == 401


def test_user_sees_only_own_tasks(client):
    make_task(client, user_id="10", title="User 10 task")
    make_task(client, user_id="20", title="User 20 task")

    response = client.get("/tasks", headers={"X-User-Id": "10"})

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["User 10 task"]


def test_filter_tasks_by_status_and_min_priority(client):
    make_task(client, title="Low todo", status="todo", priority=2)
    make_task(client, title="High todo", status="todo", priority=5)
    make_task(client, title="High done", status="done", priority=5)

    response = client.get(
        "/tasks?status=todo&min_priority=4",
        headers={"X-User-Id": "10"},
    )

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["High todo"]


def test_update_task_status_success(client):
    task_id = make_task(client).json()["id"]

    response = client.patch(
        f"/tasks/{task_id}/status",
        json={"status": "done"},
        headers={"X-User-Id": "10"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_get_foreign_or_missing_task_returns_404(client):
    task_id = make_task(client, user_id="20").json()["id"]

    foreign_response = client.get(f"/tasks/{task_id}", headers={"X-User-Id": "10"})
    missing_response = client.get("/tasks/999", headers={"X-User-Id": "10"})

    assert foreign_response.status_code == 404
    assert missing_response.status_code == 404


def test_delete_task_success(client):
    task_id = make_task(client).json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers={"X-User-Id": "10"})
    list_response = client.get("/tasks", headers={"X-User-Id": "10"})

    assert response.status_code == 204
    assert list_response.json() == []
