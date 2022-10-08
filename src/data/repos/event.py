from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.data.models.user.event import Event, UserEvent
from src.data.repos.base import BaseRepo


class EventRepo(BaseRepo):

    async def get_all(self):
        return (
            await self.session.execute(
                select(
                    Event
                ).options(
                    selectinload(UserEvent)
                )
            )
        ).scalars().all()
