from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
import enum

from sqlmodel import SQLModel, Field, Enum, Column, Relationship
from src.data.models.user.user_event import UserEvent
if TYPE_CHECKING:
    from src.data.models.user.event import Event


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"
    creator = "creator"


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(unique=True)
    email: str
    full_name: str = None
    password: str
    position: str = None
    balance: int = 0
    is_active: bool = True
    role: UserRole = Field(sa_column=Column(Enum(UserRole)), default=UserRole.user)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    events: list["Event"] = Relationship(back_populates="users", link_model=UserEvent)
    created_events: list["Event"] = Relationship(back_populates="creator")
    private_id: str | None
    public_id: str | None
