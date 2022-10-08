import abc


class BaseUseCase(abc.ABC):

    @abc.abstractmethod
    async def get_all(self):
        ...

    @abc.abstractmethod
    async def get_one(self, obj_id: int):
        ...
