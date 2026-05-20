from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.schemas import CurrentUser

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=CurrentUser)
def get_me(user: Annotated[CurrentUser, Depends(get_current_user)]):
    return user


@router.get("/{user_id}", response_model=CurrentUser)
def get_user(user_id: int):
    return CurrentUser(id=user_id, role="user")
