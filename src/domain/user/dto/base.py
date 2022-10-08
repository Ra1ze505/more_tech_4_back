from datetime import datetime

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from src.data.models.user.user import UserRole


class UserBaseSchema(BaseModel):
    id: int
    username: str
    email: str
    position: str
    balance: int
    is_active: bool
    role: UserRole
    private_id: str | None
    public_id: str | None
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
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    role: UserRole | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token", )
