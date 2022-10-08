from pydantic import parse_obj_as
from sqlalchemy import select

from src.data.models.user import User
from src.data.repos.base import BaseRepo
from src.domain.user.dto.base import UserBaseSchema

class BaseUserRepo(BaseRepo):

    async def get_user_by_username(self, username: str) -> UserBaseSchema:
        stmt = select(User).where(User.username == username)
        user = (await self.session.execute(stmt)).scalars().one()
        return parse_obj_as(UserBaseSchema, user)