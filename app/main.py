import os

from fastapi import FastAPI

from app.routers import tasks

app = FastAPI(title="Control Work 5 API")
app.include_router(tasks.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "env": os.getenv("APP_ENV", "local")}
