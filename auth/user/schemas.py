

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8 )

class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: str | datetime | None

    model_config = ConfigDict(from_attributes=True)
