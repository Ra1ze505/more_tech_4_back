from fastapi import APIRouter

from src.containers.container import container
from src.domain.marketplace.admin_item.dto.base import AdminItemBaseSchema
from src.domain.marketplace.admin_item.use_case import AdminItemUseCase
from src.domain.marketplace.event.dto.base import EventBaseSchema
from src.domain.marketplace.event.use_case import EventUseCase

marketplace_router = APIRouter(prefix="/marketplace", tags=["marketplace"])


@marketplace_router.get("/admin_item/all")
async def get_all_admin_item() -> list[AdminItemBaseSchema]:
    service: AdminItemUseCase = container.use_cases.admin_item()
    return await service.get_all()


@marketplace_router.get("/admin_item")
async def get_admin_item(item_id: int) -> AdminItemBaseSchema:
    service: AdminItemUseCase = container.use_cases.admin_item()
    return await service.get_one(obj_id=item_id)


@marketplace_router.post("/admin_item")
async def create_admin_item(item: AdminItemBaseSchema):
    service: AdminItemUseCase = container.use_cases.admin_item()
    return await service.create(data=item.dict())


@marketplace_router.get("/event/all")
async def get_all_event() -> list[EventBaseSchema]:
    service: EventUseCase = container.use_cases.event()
    return await service.get_all()


@marketplace_router.get("/event")
async def get_event(item_id: int) -> EventBaseSchema:
    service: EventUseCase = container.use_cases.event()
    return await service.get_one(obj_id=item_id)


@marketplace_router.post("/event")
async def create_event(item: EventBaseSchema):
    service: EventUseCase = container.use_cases.event()
    return await service.create(data=item.dict())
