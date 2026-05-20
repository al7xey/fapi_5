from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.dependencies import get_current_user, get_storage
from app.schemas import CurrentUser, TaskCreate, TaskRead, TaskStatus, TaskStatusUpdate
from app.storage import TaskStorage

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    user: Annotated[CurrentUser, Depends(get_current_user)],
    storage: Annotated[TaskStorage, Depends(get_storage)],
):
    return storage.create_task(payload, owner_id=user.id)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    user: Annotated[CurrentUser, Depends(get_current_user)],
    storage: Annotated[TaskStorage, Depends(get_storage)],
    task_status: Annotated[TaskStatus | None, Query(alias="status")] = None,
    min_priority: int | None = Query(default=None, ge=1, le=5),
):
    return storage.list_tasks(
        owner_id=user.id,
        status=task_status,
        min_priority=min_priority,
    )


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    user: Annotated[CurrentUser, Depends(get_current_user)],
    storage: Annotated[TaskStorage, Depends(get_storage)],
):
    task = storage.get_task(task_id)
    if task is None or task.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.patch("/{task_id}/status", response_model=TaskRead)
def update_task_status(
    task_id: int,
    payload: TaskStatusUpdate,
    user: Annotated[CurrentUser, Depends(get_current_user)],
    storage: Annotated[TaskStorage, Depends(get_storage)],
):
    task = storage.get_task(task_id)
    if task is None or task.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return storage.update_status(task_id, payload.status)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user: Annotated[CurrentUser, Depends(get_current_user)],
    storage: Annotated[TaskStorage, Depends(get_storage)],
):
    task = storage.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    storage.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
