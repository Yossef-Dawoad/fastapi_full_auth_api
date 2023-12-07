
from datetime import datetime, timezone

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from auth.exceptions.error_exceptions import bad_exception400
from auth.user.email import (
    VERIFY_ACCOUNT_CTX,
    send_request_verification_email,
    send_welcome_successful_activation_email,
)
from auth.user.models import User
from auth.user.schemas import UserCreateSchema, UserVerifySchema
from auth.user.security import is_password_strong, verify_password


async def create_user_service(
    user: UserCreateSchema,
    background_tasks: BackgroundTasks,
    session: Session,
) -> User:
    user_exist = session.query(User).filter(User.email == user.email).first()
    if user_exist: raise bad_exception400(msg='Email is already Exists.')
    if not is_password_strong(user.password):
        raise bad_exception400(
            "try compination of Upper and digit "
            "with special chracters in your password",
        )

    new_user = User(**user.model_dump())
    new_user.updated_at = datetime.now(tz=timezone.utc)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    await send_request_verification_email(new_user, background_tasks=background_tasks)
    return new_user

async def activate_user_acc(
        userIn: UserVerifySchema,
        background_tasks: BackgroundTasks,
        session: Session,
) -> None:
    user_db = session.query(User).filter(User.email == userIn.email).first()
    if not user_db: raise bad_exception400(msg='Email is not Exists.')
    user_token = user_db.user_ctx_token(context=VERIFY_ACCOUNT_CTX)
    if not verify_password(user_token, userIn.token):
        raise bad_exception400(msg='Invalid Token')

    user_db.is_active =True
    user_db.updated_at = datetime.now(tz=timezone.utc)
    user_db.verified_at =datetime.now(tz=timezone.utc)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    await send_welcome_successful_activation_email(user_db, background_tasks=background_tasks)
