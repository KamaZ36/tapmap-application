from httpx import AsyncClient

from typing import Any

from app.services.http_client.base import BaseHttpClient


class HttpClient(BaseHttpClient):
    
    async def get(self, url: str, params: dict | None = None, headers: dict | None = None) -> dict[str, Any]:
        async with AsyncClient() as client: 
            response = await client.get(url=url, params=params)
        if response.status_code != 200: 
            #TODO ДОПИЛИТЬ
            pass
        return response.json()
        
        
http_client = HttpClient()    
