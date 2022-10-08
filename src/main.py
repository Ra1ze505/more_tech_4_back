import time
from typing import Any

from fastapi import FastAPI, Request
from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware

from src.api.v1.router.user import user_router
from src.containers.container import container


def create_app() -> FastAPI:
    application = FastAPI(
        title=container.config.app_name(),
        root_path=container.config.app.root_path(),
        debug=container.config.app.debug(),
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    container.gateways.logging_setup.init()  # type: ignore
    application.include_router(user_router, prefix="/api/v1")
    application.container = container
    return application


app = create_app()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Any) -> Response:
    """Измерение скорости процесса выполнения запроса."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.on_event("startup")
async def startup_event() -> None:
    await app.container.init_resources()  # type: ignore


@app.on_event("startup")
@repeat_every(seconds=1)  # 1 hour
async def check_transactions() -> None:
    use_case = container.use_cases.check_status()
    await use_case()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await app.container.shutdown_resources()  # type: ignore


if __name__ == "__main__":
    import uvicorn  # type: ignore[import]

    uvicorn.run(app=app, host="0.0.0.0", port=8000, log_level="info")
