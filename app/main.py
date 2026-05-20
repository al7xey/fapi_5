import os

from fastapi import FastAPI

from app.routers import admin, rooms, tasks, users

app = FastAPI(title="Control Work 5 API")
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(rooms.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "env": os.getenv("APP_ENV", "local")}
