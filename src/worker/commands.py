from functools import wraps
from typing import Callable, Any

import anyio
from loguru import logger

import typer

from src.containers.container import container
from src.data.repos.polygon.transfer import TransferApiRepo
from src.data.repos.polygon.wallet import WalletApiRepo
from src.domain.exceptions.polygon import PolygonException

app = typer.Typer()


def run_async(func: Callable) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
        async def coro_wrapper() -> Any:
            return await func(*args, **kwargs)

        return anyio.run(coro_wrapper)

    return wrapper


async def on_startup() -> None:
    await container.init_resources()  # type: ignore
    container.gateways.logging_setup.init()
    logger.info("Init resources")


@app.command()
@run_async
async def test(self) -> None:
    from rich import print
    await on_startup()
    wallet_repo: WalletApiRepo = await container.repos.wallet_repo()
    transfer_repo: TransferApiRepo = await container.repos.transfer_repo()
    conf: dict = container.config.polygon()
    wallet = await wallet_repo.new()
    wallet_2 = await wallet_repo.new()
    # print(await wallet_repo.balance(wallet.public_key))
    # print(await wallet_repo.balance_nft(wallet.public_key))
    # print(await wallet_repo.history(wallet.public_key))
    print(await wallet_repo.balance(conf.get('public_key')))
    # print(await wallet_repo.balance_nft(conf.get('public_key')))
    #
    # print(await wallet_repo.history(conf.get('public_key')))

    # print(conf)
    try:
        res = await transfer_repo.transfer_ruble(conf.get('private_key'), wallet_2.public_key, 0.1)
        print(res)
    except PolygonException as e:
        print(e)



if __name__ == "__main__":
    app()

