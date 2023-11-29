from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String

from auth.db import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(150))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    mobile = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    verified_at = Column(DateTime, default=False)  
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now, nullable=True)