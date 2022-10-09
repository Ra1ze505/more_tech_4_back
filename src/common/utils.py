from functools import wraps
from typing import Any, Callable

import anyio


def run_async(func: Callable) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
        async def coro_wrapper() -> Any:
            return await func(*args, **kwargs)

        return anyio.run(coro_wrapper)

    return wrapper
