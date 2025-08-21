from httpx import AsyncClient, HTTPError

from typing import Any

from app.services.http_client.base import BaseHttpClient


class HttpClient(BaseHttpClient):
    
    async def get(self, url: str, params: dict | None = None, headers: dict | None = None) -> dict[str, Any]:
        try:
            async with AsyncClient() as client:
                response = await client.get(url=url, params=params, headers=headers)
                response.raise_for_status()
                return response.json()
        except HTTPError as exc:
            # Пробрасываем дальше; адаптер геокодера решит, как маппить
            raise
        
        
http_client = HttpClient()    
