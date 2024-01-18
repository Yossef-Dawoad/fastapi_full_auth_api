

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8)

class  UserVerifySchema(BaseModel):
    email: EmailStr
    token: str

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: str | datetime | None

    model_config = ConfigDict(from_attributes=True)

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str
    exp: int = None
