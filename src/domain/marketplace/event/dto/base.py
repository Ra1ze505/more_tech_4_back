from datetime import date, datetime, time

from pydantic import BaseModel

from src.data.models.user import User


class EventBaseSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: date | None = None
    start_time: time | None = None
    end_date: date | None = None
    end_time: time | None = None
    repeat: bool | None = None
    is_active: bool | None = None
    creator_id: int | None = None
    creator: int | None = None
    users: list[int] | None = None
    base_price: int | None = None
    price: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class EventOutSchema(EventBaseSchema):
    id: int
