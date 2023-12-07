from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from auth.confdb import Base
from auth.user import security


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(150))
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # nullable or default values
    mobile = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now, nullable=True)

    def __init__(self, password: str, *args:tuple, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.password = security.get_str_hash(password)

    def verify_password(self, password: str) -> bool:
        return security.verify_password(password, self.password)

    def user_ctx_token(self, context: str) -> str:
        """
        unique token for each user used in somthing like email verification

        :param context:
            is any arabtray string that maybe resamble the contex you want
            to use teh user token in.
        e.g.::

            # for email verification
            user = User(**kwargs)
            token = user.user_ctx_token('email verification')
        """
        return f"""
                {context}{self.password[-6:]}{self.updated_at.strftime('%m%d%Y%H%M%S')}
                """.strip()
