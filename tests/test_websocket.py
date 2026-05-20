import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.room_manager import room_manager


@pytest.fixture(autouse=True)
def clean_rooms():
    room_manager.reset()
    yield
    room_manager.reset()


@pytest.fixture
def client():
    return TestClient(app)


def test_connect_to_room_with_valid_username(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        assert websocket.receive_json() == {
            "type": "connect",
            "room_id": "python",
            "username": "alice",
        }
        response = client.get("/rooms/python/users")
        assert response.json() == {"room_id": "python", "users": ["alice"]}


def test_send_message_and_receive_response(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        websocket.receive_json()
        websocket.send_json({"type": "message", "text": "Hello"})

        assert websocket.receive_json() == {
            "type": "message",
            "room_id": "python",
            "username": "alice",
            "text": "Hello",
        }


def test_two_clients_in_same_room_receive_same_message(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as alice:
        alice.receive_json()
        with client.websocket_connect("/ws/rooms/python?username=bob") as bob:
            alice.receive_json()
            bob.receive_json()

            alice.send_json({"type": "message", "text": "Hi Bob"})

            expected = {
                "type": "message",
                "room_id": "python",
                "username": "alice",
                "text": "Hi Bob",
            }
            assert alice.receive_json() == expected
            assert bob.receive_json() == expected


def test_users_from_different_rooms_are_listed_separately(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as alice:
        alice.receive_json()
        with client.websocket_connect("/ws/rooms/js?username=bob") as bob:
            bob.receive_json()

            assert client.get("/rooms/python/users").json() == {
                "room_id": "python",
                "users": ["alice"],
            }
            assert client.get("/rooms/js/users").json() == {
                "room_id": "js",
                "users": ["bob"],
            }


def test_too_long_message_returns_error(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        websocket.receive_json()
        websocket.send_json({"type": "message", "text": "x" * 301})

        assert websocket.receive_json() == {
            "type": "error",
            "detail": "Message is too long",
        }


def test_disconnected_user_is_removed_from_room(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        websocket.receive_json()

    assert client.get("/rooms/python/users").json() == {"room_id": "python", "users": []}
