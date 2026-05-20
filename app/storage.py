from app.schemas import TaskCreate, TaskRead, TaskStatus


class TaskStorage:
    def __init__(self) -> None:
        self._tasks: dict[int, TaskRead] = {}
        self._next_id = 1

    def reset(self) -> None:
        self._tasks.clear()
        self._next_id = 1

    def create_task(self, payload: TaskCreate, owner_id: int) -> TaskRead:
        task = TaskRead(id=self._next_id, owner_id=owner_id, **payload.model_dump())
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def list_tasks(
        self,
        owner_id: int | None = None,
        status: TaskStatus | None = None,
        min_priority: int | None = None,
    ) -> list[TaskRead]:
        tasks = list(self._tasks.values())
        if owner_id is not None:
            tasks = [task for task in tasks if task.owner_id == owner_id]
        if status is not None:
            tasks = [task for task in tasks if task.status == status]
        if min_priority is not None:
            tasks = [task for task in tasks if task.priority >= min_priority]
        return tasks

    def get_task(self, task_id: int) -> TaskRead | None:
        return self._tasks.get(task_id)

    def update_status(self, task_id: int, status: TaskStatus) -> TaskRead:
        task = self._tasks[task_id]
        updated = task.model_copy(update={"status": status})
        self._tasks[task_id] = updated
        return updated

    def delete_task(self, task_id: int) -> None:
        del self._tasks[task_id]

    def stats(self) -> dict[str, object]:
        by_status = {status.value: 0 for status in TaskStatus}
        for task in self._tasks.values():
            by_status[task.status.value] += 1
        return {"total_tasks": len(self._tasks), "by_status": by_status}


task_storage = TaskStorage()
