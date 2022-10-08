from sqlalchemy import select

from src.data.models.marketplace.admin_item import AdminItem
from src.data.repos.base import BaseRepo


class AdminItemRepo(BaseRepo):

    async def get_all(self):
        return (await self.session.execute(select(AdminItem))).scalars().all()

    async def get_one(self, obj_id: int):
        return (
            await self.session.execute(
                select(AdminItem).where(
                    AdminItem.id == obj_id
                )
            )
        ).scalars().one()
