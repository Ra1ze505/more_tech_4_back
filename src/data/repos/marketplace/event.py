from http.client import HTTPException

from pydantic import parse_obj_as
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.data.models.marketplace.event import Event
from src.data.repos.base import BaseRepo
from src.domain.marketplace.event.dto.base import EventBaseSchema, EventInSchema, EventOutSchema


class EventRepo(BaseRepo):
    model = Event
    query = select(Event)
    schema = EventBaseSchema
    out_schema = EventOutSchema
