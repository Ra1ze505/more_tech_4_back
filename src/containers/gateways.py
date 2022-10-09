from dependency_injector import containers, providers
from httpx import AsyncClient

from src.common.db import Database
from src.common.http_client import init_async_http_client
from src.common.logging import setup_logging


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
