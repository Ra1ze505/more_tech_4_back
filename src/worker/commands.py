import typer
from loguru import logger

from src.common.utils import run_async
from src.containers.container import container

app = typer.Typer()


async def on_startup() -> None:
    await container.init_resources()  # type: ignore
    container.gateways.logging_setup.init()
    logger.info("Init resources")


@app.command()
@run_async
async def test(self) -> None:
    await on_startup()


if __name__ == "__main__":
    app()
