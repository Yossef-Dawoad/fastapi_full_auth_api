from typing import Annotated, TypeAlias

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from auth.confdb import get_db
from auth.user.schemas import UserCreateSchema, UserResponseSchema
from auth.user.services import create_user_service

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

dbDepType: TypeAlias = Annotated[Session, Depends(get_db)]

@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseSchema,
)
async def create_user(
    user: UserCreateSchema,
    background_tasks: BackgroundTasks,
    db: dbDepType,
) -> UserResponseSchema:
    return await create_user_service(user, background_tasks, db)
