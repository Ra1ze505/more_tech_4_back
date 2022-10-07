
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.domain.user import UserService
from src.containers.container import container

user_router = APIRouter(prefix='/user', tags=['user'])


@user_router.get("/all")
async def get_all():
    service = container.use_cases.user()
    return await service.get_all()