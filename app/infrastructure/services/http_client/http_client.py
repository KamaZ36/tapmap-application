from httpx import AsyncClient, HTTPError
from typing import Any

from app.infrastructure.services.http_client.base import BaseHttpClient


class HttpClient(BaseHttpClient):
    def __init__(self) -> None:
        self._client = AsyncClient()

    async def get(
        self, url: str, params: dict | None = None, headers: dict | None = None
    ) -> dict[str, Any]:
        try:
            response = await self._client.get(url=url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except HTTPError as exc:
            # Пробрасываем дальше; адаптер геокодера решит, как маппить
            raise

    async def close(self) -> None:
        await self._client.aclose()
