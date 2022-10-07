from datetime import datetime

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from src.data.models.user import UserRole


class UserBaseSchema(BaseModel):
    id: int
    username: str
    email: str
    password: str
    position: str
    balance: int
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str
    position: str
    balance: int
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token", )
