from datetime import datetime
import enum

from sqlmodel import SQLModel, Field, Enum, Column


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"
    creator = "creator"


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    full_name: str = None
    password: str
    position: str = None
    balance: int = 0
    is_active: bool = True
    role: UserRole = Field(sa_column=Column(Enum(UserRole)), default=UserRole.user)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)