from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr, validator

from src.common.schema import BaseSchema, OrmSchema
from src.data.models.user.user import UserRole


class UserBaseSchema(BaseSchema):
    id: UUID
    username: str
    email: EmailStr
    password: SecretStr
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime


class UserOutSchema(UserBaseSchema, OrmSchema):
    ...


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr
    full_name: str

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return v

    @validator("username")
    def validate_username(cls, v):
        if len(v) < 4:
            raise ValueError("Username must be at least 4 characters.")
        return v
