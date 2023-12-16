
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic_core import ValidationError
from sqlalchemy.orm import Session

from auth.confsettings import get_settings
from auth.exceptions.error_exceptions import (
    bad_exception400,
    notfound_exception404,
    unauthorized_exception401,
)
from auth.user.email import (
    VERIFY_ACCOUNT_CTX,
    send_request_verification_email,
    send_welcome_successful_activation_email,
)
from auth.user.models import User, UserToken
from auth.user.schemas import (
    TokenPayload,
    TokenSchema,
    UserCreateSchema,
    UserVerifySchema,
)
from auth.user.security import (
    is_password_strong,
    verify_password,
)

settings = get_settings()

async def get_user(db: Session, user_name: str) -> User | None:
    return db.query(User).filter(User.email == user_name).first()


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


async def user_login_service(
    userIn:OAuth2PasswordRequestForm,
    session: Session,
) -> TokenSchema:
    if not (user_exists := session.query(User).filter(User.email == userIn.username).first()):
        raise bad_exception400(msg='Email is not Exists.')
    if not verify_password(userIn.password, user_exists.password):
        raise bad_exception400(msg='Invalid Email or Password')

    # populate user token and refresh token in user_token table
    user_token = UserToken(
        user_id=user_exists.id,
        access_token = create_access_token(user_exists.email),
        refresh_token = create_refresh_token(user_exists.email),
        expires_at=datetime.now(tz=timezone.utc) + timedelta(minutes=30),
    )
    session.add(user_token)
    session.commit()
    session.refresh(user_token)

    return {
        "access_token": user_token.access_token,
        "refresh_token": user_token.refresh_token,
        "token_type": "bearer",
    }




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def create_access_token(
    subject: str | None,
    expires_delta: timedelta | None = None,
) -> str:
    if not expires_delta: expires_delta = timedelta(minutes=30)
    expire_time = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire_time, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt

def create_refresh_token(
    subject: str | None,
    expires_delta: timedelta | None = None,
) -> str:
    if not expires_delta: expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_TIME)
    expire_time = datetime.now(tz=timezone.utc) + expires_delta
    to_encode = {"exp": expire_time, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_refresh_secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


async def get_refresh_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session,
) -> TokenSchema:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise unauthorized_exception401(
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user(db, user_name=token_data.sub)

    if user is None:
        raise notfound_exception404(detail="Invalid token for user")
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
        "token_type": "brearer",
    }
