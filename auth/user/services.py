
from sqlalchemy.orm import Session

from auth.user.models import User
from auth.user.schemas import UserCreateSchema


async def create_user_service(user: UserCreateSchema, db: Session) -> User:
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
