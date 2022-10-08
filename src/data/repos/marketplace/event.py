from sqlalchemy import select

from src.data.models.marketplace.event import Event
from src.data.repos.base import BaseRepo


class EventRepo(BaseRepo):
    async def get_all(self):
        return (await self.session.execute(select(Event))).scalars().all()

    async def get_one(self, obj_id: int):
        return (await self.session.execute(select(Event).where(Event.id == obj_id))).scalars().one()
