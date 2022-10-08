import logging
import sys
from typing import AsyncGenerator

import httpx
import loguru
from dependency_injector import containers, providers
from httpx import AsyncClient

from src.data.db.db import Database


async def init_async_http_client(
    base_url: str,
) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Инициализация асинхронного http-клиента"""
    async with httpx.AsyncClient(base_url=base_url) as client:
        yield client


class InterceptHandler(logging.Handler):
    """Решение из официальной документации https://readthedocs.org/projects/loguru/downloads/pdf/stable/"""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = loguru.logger.level(record.levelname).name
        except ValueError:
            level = record.levelno  # type: ignore
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1
        loguru.logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(config: dict) -> None:
    """Очистка логгера и обнуление корневого хендлера для stdout и stderr"""
    loguru.logger.remove()
    logging.root.handlers = []
    logging.root.setLevel(config["level"])
    for name in logging.root.manager.loggerDict.keys():
        """Очистка хендлеров для каждой либы(при их наличии) и определение кастомного хендлера"""
        if logging.getLogger(name).hasHandlers():
            logging.getLogger(name).handlers.clear()
        logging.getLogger(name).handlers = [InterceptHandler()]
        logging.getLogger(name).propagate = False
    loguru.logger.configure(handlers=[{"sink": sys.stdout, "serialize": config["serializer"]}])


class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Singleton(Database, config.db)

    logging_setup: providers.Provider[None] = providers.Resource(
        setup_logging, config=config.logging
    )

    # Http Clients
    http_client: providers.Provider[AsyncClient] = providers.Resource(
        init_async_http_client,
        base_url="",
    )
