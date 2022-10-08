from sqlalchemy import select

from src.data.models.marketplace.event import Event
from src.data.repos.base import BaseRepo
from src.domain.marketplace.event.dto.base import EventBaseSchema, EventOutSchema


class EventRepo(BaseRepo):
    model = Event
    query = select(Event)
    schema = EventBaseSchema
    out_schema = EventOutSchema
