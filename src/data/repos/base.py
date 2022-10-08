import abc
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.db.db import Database


class BaseRepo:

    def __init__(self, db: Database):
        self.db = db

    @property
    def session(self) -> AsyncSession:
        return self.db.session

    @abc.abstractmethod
    async def get_all(self):
        ...

    @abc.abstractmethod
    async def get_one(self, obj_id: int):
        ...
