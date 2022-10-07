from httpx import AsyncClient, Request
from starlette import status

from src.domain.exceptions.polygon import PolygonException

transaction_hash = str


class PolygonBaseRepo:
    def __init__(self, http_client: AsyncClient, config: dict):
        self.base_url = 'https://hackathon.lsp.team/hk/v1'
        self.http_client = http_client
        self.public_key = config["public_key"]
        self.private_key = config["private_key"]

    async def send(self, request: Request) -> dict:
        response = await self.http_client.send(request)
        if response.status_code not in {status.HTTP_200_OK, status.HTTP_201_CREATED}:
            detail = response.json()
            detail['url'] = request.url
            detail['method'] = request.method
            raise PolygonException(detail)
        return response.json()

    @property
    def headers(self) -> dict:
        return {
            # 'Content-Type': 'application/json',
            # 'Accept': 'application/json',
        }
