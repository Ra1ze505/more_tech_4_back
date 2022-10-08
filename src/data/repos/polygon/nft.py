from httpx import AsyncClient
from pydantic import parse_obj_as

from src.data.repos.polygon.base import PolygonBaseRepo, transaction_hash
from src.domain.polygon.dto.base import GeneratedNftSchema, NftSchema


class NftApiRepo(PolygonBaseRepo):
    def __init__(self, http_client: AsyncClient, config: dict):
        super().__init__(http_client, config)
        self.base_url = self.base_url + "/nft"

    async def generate(self, to_public_key: str, uri: str, count: int = 1) -> transaction_hash:
        request = self.http_client.build_request(
            method="POST",
            url=f"{self.base_url}/generate",
            data={
                "toPublicKey": to_public_key,
                "uri": uri,
                "nftCount": count,
            },
            headers=self.headers,
        )
        response = await self.send(request)
        return response.get("transactionHash")

    async def get_generate(self, transaction_hash: str) -> GeneratedNftSchema:
        request = self.http_client.build_request(
            method="GET",
            url=f"{self.base_url}/generate/{transaction_hash}",
            headers=self.headers,
        )
        response = await self.send(request)
        return parse_obj_as(GeneratedNftSchema, response)

    async def info(self, nft_token: str) -> NftSchema:
        request = self.http_client.build_request(
            method="GET", url=f"{self.base_url}/{nft_token}", headers=self.headers
        )
        response = await self.send(request)
        return parse_obj_as(NftSchema, response)
