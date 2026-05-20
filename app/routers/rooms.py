from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from app.room_manager import room_manager

router = APIRouter(tags=["rooms"])


@router.websocket("/ws/rooms/{room_id}")
async def room_chat(websocket: WebSocket, room_id: str, username: str | None = None):
    if username is None or not username.strip():
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    username = username.strip()
    await room_manager.connect(room_id, username, websocket)
    try:
        while True:
            payload = await websocket.receive_json()
            text = payload.get("text", "")
            if len(text) > 300:
                await websocket.send_json(
                    {"type": "error", "detail": "Message is too long"}
                )
                continue

            if payload.get("type") == "message":
                await room_manager.broadcast(
                    room_id,
                    {
                        "type": "message",
                        "room_id": room_id,
                        "username": username,
                        "text": text,
                    },
                )
    except WebSocketDisconnect:
        room_manager.disconnect(room_id, username, websocket)


@router.get("/rooms/{room_id}/users")
def get_room_users(room_id: str):
    return {"room_id": room_id, "users": room_manager.get_users(room_id)}
