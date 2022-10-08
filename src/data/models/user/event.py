from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime, time, date

from sqlmodel import SQLModel, Field, Relationship
from src.data.models.user.user_event import UserEvent

if TYPE_CHECKING:
    from src.data.models.user.user import User


class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    description: str = Field(default=None)
    start_date: date
    start_time: time
    end_date: date
    end_time: time
    repeat: bool = Field(default=False)
    is_active: bool = Field(default=True)
    creator_id: int = Field(foreign_key="user.id")
    creator: User = Relationship(back_populates="created_events")
    users: list[User] = Relationship(back_populates="events", link_model=UserEvent)
    base_price: int = Field(default=0)
    price: int = Field(default=0)
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)
