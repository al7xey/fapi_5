from typing import Annotated

from fastapi import Header, HTTPException, status

from app.schemas import CurrentUser
from app.storage import task_storage


def get_current_user(
    x_user_id: Annotated[str | None, Header(alias="X-User-Id")] = None,
    x_user_role: Annotated[str, Header(alias="X-User-Role")] = "user",
) -> CurrentUser:
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-User-Id header",
        )

    try:
        user_id = int(x_user_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-User-Id header",
        ) from exc

    return CurrentUser(id=user_id, role=x_user_role)


def require_admin(user: Annotated[CurrentUser, get_current_user]) -> CurrentUser:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )
    return user


def get_storage():
    return task_storage
