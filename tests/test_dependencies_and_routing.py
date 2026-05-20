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


def create_task(client, user_id="10", status="todo", priority=3):
    return client.post(
        "/tasks",
        json={
            "title": f"Task {status} {priority}",
            "description": None,
            "status": status,
            "priority": priority,
        },
        headers={"X-User-Id": user_id},
    )


def test_users_me_returns_current_user(client):
    response = client.get(
        "/users/me",
        headers={"X-User-Id": "10", "X-User-Role": "admin"},
    )

    assert response.status_code == 200
    assert response.json() == {"id": 10, "role": "admin"}


def test_missing_user_id_returns_401(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_regular_user_gets_403_for_admin_stats(client):
    response = client.get(
        "/admin/stats",
        headers={"X-User-Id": "10", "X-User-Role": "user"},
    )

    assert response.status_code == 403


def test_admin_gets_stats_for_all_tasks(client):
    create_task(client, user_id="10", status="todo", priority=1)
    create_task(client, user_id="20", status="todo", priority=2)
    create_task(client, user_id="20", status="in_progress", priority=3)
    create_task(client, user_id="30", status="done", priority=4)
    create_task(client, user_id="30", status="done", priority=5)

    response = client.get(
        "/admin/stats",
        headers={"X-User-Id": "99", "X-User-Role": "admin"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "total_tasks": 5,
        "by_status": {"todo": 2, "in_progress": 1, "done": 2},
    }


def test_regular_user_cannot_delete_foreign_task_via_tasks_router(client):
    task_id = create_task(client, user_id="20").json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers={"X-User-Id": "10"})

    assert response.status_code == 403


def test_admin_can_delete_foreign_task(client):
    task_id = create_task(client, user_id="20").json()["id"]

    response = client.delete(
        f"/admin/tasks/{task_id}",
        headers={"X-User-Id": "99", "X-User-Role": "admin"},
    )

    assert response.status_code == 204
    assert client.get("/tasks", headers={"X-User-Id": "20"}).json() == []


def test_openapi_routes_are_grouped_by_tags(client):
    paths = client.get("/openapi.json").json()["paths"]

    assert paths["/tasks"]["post"]["tags"] == ["tasks"]
    assert paths["/users/me"]["get"]["tags"] == ["users"]
    assert paths["/admin/stats"]["get"]["tags"] == ["admin"]
