from httpx import AsyncClient, HTTPError, Limits, Timeout
from typing import Any

from app.infrastructure.services.http_client.base import BaseHttpClient


class HttpClient(BaseHttpClient):
    def __init__(self) -> None:
        limits = Limits(
            max_keepalive_connections=20,
            max_connections=50,
            keepalive_expiry=30.0,
        )

        timeout = Timeout(connect=5.0, read=10.0, write=5.0, pool=5.0)

        self._client = AsyncClient(
            limits=limits, timeout=timeout, http2=True, follow_redirects=True
        )

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
