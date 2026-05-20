from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class CurrentUser(BaseModel):
    id: int
    role: str = "user"


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    description: str | None = None
    status: TaskStatus = TaskStatus.todo
    priority: int = Field(ge=1, le=5)


class TaskRead(TaskCreate):
    id: int
    owner_id: int


class TaskStatusUpdate(BaseModel):
    status: TaskStatus
