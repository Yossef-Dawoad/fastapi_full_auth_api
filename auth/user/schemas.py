

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: str | datetime | None

    model_config = ConfigDict(from_attributes=True)
