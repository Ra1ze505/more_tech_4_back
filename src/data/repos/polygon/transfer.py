from httpx import AsyncClient

from src.data.repos.polygon.base import PolygonBaseRepo, transaction_hash


class TransferApiRepo(PolygonBaseRepo):
    def __init__(self, http_client: AsyncClient, config: dict):
        super().__init__(http_client, config)
        self.base_url = self.base_url + "/transfers"

    async def transfer_matic(
        self, from_private_key: str, to_public_key: str, amount: float
    ) -> transaction_hash:
        request = self.http_client.build_request(
            method="POST",
            url=f"{self.base_url}/matic",
            data={
                "fromPrivateKey": from_private_key,
                "toPublicKey": to_public_key,
                "amount": amount,
            },
        )
        response = await self.send(request)
        return response.get("transaction")

    async def transfer_ruble(
        self, from_private_key: str, to_public_key: str, amount: float
    ) -> transaction_hash:
        request = self.http_client.build_request(
            method="POST",
            url=f"{self.base_url}/ruble",
            data={
                "fromPrivateKey": from_private_key,
                "toPublicKey": to_public_key,
                "amount": amount,
            },
        )
        response = await self.send(request)
        return response.get("transaction")

    async def transfer_nft(
        self, from_private_key: str, to_public_key: str, token_id: int
    ) -> transaction_hash:
        request = self.http_client.build_request(
            method="POST",
            url=f"{self.base_url}/nft",
            data={
                "fromPrivateKey": from_private_key,
                "toPublicKey": to_public_key,
                "tokenId": token_id,
            },
        )
        response = await self.send(request)
        return response.get("transaction")

    async def transfer_status(self, transaction_hash: str) -> dict:
        # todo {"status": "Success" }
        request = self.http_client.build_request(
            method="GET",
            url=f"{self.base_url}/status/{transaction_hash}",
        )
        response = await self.send(request)
        return response
