from fastapi import FastAPI

from app.routers import tasks

app = FastAPI(title="Control Work 5 API")
app.include_router(tasks.router)
