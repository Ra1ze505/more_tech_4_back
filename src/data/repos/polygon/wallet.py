from httpx import AsyncClient, Request
from pydantic import parse_obj_as
from starlette import status

from src.data.repos.polygon.base import PolygonBaseRepo
from src.domain.exceptions.polygon import PolygonException
from src.domain.polygon.dto.base import (
    WalletBalanceNftSchema,
    WalletBalanceSchema,
    WalletCreatedSchema,
    WalletHistorySchema,
)


class WalletApiRepo(PolygonBaseRepo):
    def __init__(self, http_client: AsyncClient, config: dict):
        super().__init__(http_client, config)
        self.base_url = self.base_url + "/wallets"

    async def new(self) -> WalletCreatedSchema:
        request = self.http_client.build_request(
            method="POST", url=f"{self.base_url}/new", headers=self.headers
        )
        response = await self.send(request)
        return parse_obj_as(WalletCreatedSchema, response)

    async def balance(self, public_key: str) -> WalletBalanceSchema:
        request = self.http_client.build_request(
            method="GET",
            url=f"{self.base_url}/{public_key}/balance",
            headers=self.headers,
        )
        response = await self.send(request)
        return parse_obj_as(WalletBalanceSchema, response)

    async def balance_nft(self, public_key: str) -> WalletBalanceNftSchema:
        request = self.http_client.build_request(
            method="GET",
            url=f"{self.base_url}/{public_key}/nft/balance",
            headers=self.headers,
        )
        response = await self.send(request)
        return parse_obj_as(WalletBalanceNftSchema, response)

    async def history(
        self, public_key: str, page: int = 0, offset: int = 100, sort: str = "asc"
    ) -> WalletHistorySchema:
        request = self.http_client.build_request(
            method="POST",
            url=f"{self.base_url}/{public_key}/history",
            data={
                "page": page,
                "offset": offset,
                "sort": sort,
            },
            headers=self.headers,
        )
        response = await self.send(request)
        return parse_obj_as(WalletHistorySchema, response)
