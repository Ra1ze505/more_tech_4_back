from src.data.repos.marketplace.event import EventRepo
from src.domain.base.base_use_case import BaseUseCase


class EventUseCase(BaseUseCase):
    def __init__(self, repo: EventRepo):
        self.repo = repo

    async def get_one(self, obj_id: int):
        return await self.repo.get_one(obj_id=obj_id)

    async def get_all(self):
        return await self.repo.get_all()
