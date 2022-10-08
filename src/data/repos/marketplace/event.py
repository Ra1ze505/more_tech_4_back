from http.client import HTTPException

from pydantic import parse_obj_as
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.data.models.marketplace.event import Event
from src.data.repos.base import BaseRepo
from src.domain.marketplace.event.dto.base import EventBaseSchema, EventOutSchema


class EventRepo(BaseRepo):
    model = Event
    query = select(Event)
    schema = EventBaseSchema
    out_schema = EventOutSchema

    async def create(self, data: dict):
        obj = self.model(**data)
        self.session.add(obj)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Object already exists"
            )
        q = select(self.model).where(self.model.id == obj.id)
        obj = (await self.session.execute(q)).scalars().one()
        return parse_obj_as(self.out_schema, obj)
