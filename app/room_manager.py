from collections import defaultdict

from fastapi import WebSocket


class RoomManager:
    def __init__(self) -> None:
        self._rooms: dict[str, dict[str, list[WebSocket]]] = defaultdict(dict)

    async def connect(self, room_id: str, username: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._rooms[room_id].setdefault(username, []).append(websocket)
        await self.broadcast(
            room_id,
            {"type": "connect", "room_id": room_id, "username": username},
        )

    def disconnect(self, room_id: str, username: str, websocket: WebSocket) -> None:
        room = self._rooms.get(room_id)
        if room is None or username not in room:
            return

        connections = room[username]
        if websocket in connections:
            connections.remove(websocket)
        if not connections:
            del room[username]
        if not room:
            del self._rooms[room_id]

    async def broadcast(self, room_id: str, payload: dict) -> None:
        room = self._rooms.get(room_id, {})
        for connections in list(room.values()):
            for websocket in list(connections):
                await websocket.send_json(payload)

    def get_users(self, room_id: str) -> list[str]:
        return sorted(self._rooms.get(room_id, {}).keys())

    def reset(self) -> None:
        self._rooms.clear()


room_manager = RoomManager()
