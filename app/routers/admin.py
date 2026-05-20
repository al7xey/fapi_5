from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies import get_storage, require_admin
from app.schemas import CurrentUser
from app.storage import TaskStorage

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
def get_stats(
    _admin: Annotated[CurrentUser, Depends(require_admin)],
    storage: Annotated[TaskStorage, Depends(get_storage)],
):
    return storage.stats()


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_any_task(
    task_id: int,
    _admin: Annotated[CurrentUser, Depends(require_admin)],
    storage: Annotated[TaskStorage, Depends(get_storage)],
):
    if storage.get_task(task_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    storage.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
