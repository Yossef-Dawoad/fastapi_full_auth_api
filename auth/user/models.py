from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from auth.confdb import Base
from auth.user.security import get_str_hash, verify_password


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(150))
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # nullable or default values
    mobile = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    # DateTime frames
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now, nullable=True)

    tokens = relationship("UserToken", back_populates="user")


    def __init__(self, password: str, *args:tuple, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.password = get_str_hash(password)

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.password)

    def user_ctx_token(self, context: str) -> str:
        """
        unique token for each user used in somthing like email verification

        :param context:
            is any arabtray string that maybe resamble the context you want
            to use the user token in.
        e.g.::

            # for email verification
            user = User(**kwargs)
            token = user.user_ctx_token('email verification')
        """
        return f"""
                {context}{self.password[-6:]}{self.updated_at.strftime('%m%d%Y%H%M%S')}
                """.strip()


class UserToken(Base):
    __tablename__ = "user_token"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))

    access_token = Column(String(250), nullable=True, index=True, default=None)
    refresh_token = Column(String(250), nullable=True, index=True, default=None)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="tokens")
