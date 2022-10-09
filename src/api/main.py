import time
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.openapi.models import Response
from fastapi_utils.tasks import repeat_every
from loguru import logger
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from src.api.router import include_routers
from src.common.exceptions.base import BaseAppException
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
    container.gateways.http_client.init()  # type: ignore
    application.include_router(include_routers(), prefix="/api/v1")
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


@app.middleware("http")
async def exception_handler(request: Request, call_next: Any) -> Response:
    """Обработка исключений."""
    try:
        return await call_next(request)
    except BaseAppException as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message)
    except Exception as e:
        logger.exception(e)
        raise e


@app.on_event("startup")
async def startup_event() -> None:
    await app.container.init_resources()  # type: ignore


@app.on_event("startup")
@repeat_every(seconds=10, logger=logger)
async def example_task() -> None:
    logger.info("Example task")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await app.container.shutdown_resources()  # type: ignore


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=8000, log_level="info")
