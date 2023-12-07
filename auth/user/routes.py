from typing import Annotated, TypeAlias

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from auth.confdb import get_db
from auth.user.schemas import UserCreateSchema, UserResponseSchema, UserVerifySchema
from auth.user.services import activate_user_acc, create_user_service

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
    userIn: UserCreateSchema,
    background_tasks: BackgroundTasks,
    db: dbDepType,
) -> UserResponseSchema:
    return await create_user_service(userIn, background_tasks, db)


@router.post("/verify-account/", status_code=status.HTTP_200_OK)
async def verify_account(
    userIn: UserVerifySchema,
    background_tasks: BackgroundTasks,
    db: dbDepType,
) -> dict:
    await activate_user_acc(userIn, background_tasks, db)
    return {"msg": "Account activated successfully"}
