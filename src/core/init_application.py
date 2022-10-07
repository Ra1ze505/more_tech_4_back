from fastapi import FastAPI

from src.api.v1.hellow_world import route_hello
from src.db.db_service import init_db

application = FastAPI()

application.include_router(route_hello)
# application.include_router(route_for_couriers)


@application.on_event("startup")
async def on_startup():
    await init_db()
