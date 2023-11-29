from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from auth.db import Base
from auth.user import hashing


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(150))
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # nullable or default values
    mobile = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now, nullable=True)

    def __init__(self, password: str, *args:tuple, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.password = hashing.get_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return hashing.verify_password(password, self.password)
