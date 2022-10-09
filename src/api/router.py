from fastapi import APIRouter

from src.api.v1.router.user import user_router


def admin_routers() -> APIRouter:
    admin_router = APIRouter(prefix="/admin")
    return admin_router


def include_routers() -> APIRouter:
    main_router = APIRouter()
    main_router.include_router(user_router, prefix="/user")
    main_router.include_router(admin_routers())
    return main_router
