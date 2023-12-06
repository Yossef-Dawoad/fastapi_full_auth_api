
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from auth.exceptions.error_exceptions import bad_exception400
from auth.user.email import send_request_verification_email
from auth.user.models import User
from auth.user.schemas import UserCreateSchema
from auth.user.security import is_password_strong


async def create_user_service(
    user: UserCreateSchema,
    background_tasks: BackgroundTasks,
    db: Session,
) -> User:
    user_exist = db.query(User).filter(User.email == user.email).first()
    if user_exist: raise bad_exception400(msg='Email is already Exists.')
    if not is_password_strong(user.password):
        raise bad_exception400(
            "try compination of Upper and digit "
            "with special chracters in your password",
        )

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # await send_request_verification_email(new_user, background_tasks=background_tasks)
    return new_user
