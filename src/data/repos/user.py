from sqlalchemy import select

from src.data.models.user import User
from src.data.repos.base import BaseRepo


class UserRepo(BaseRepo):

    async def get_all(self):
        return (await self.session.execute(select(User))).scalars().all()
