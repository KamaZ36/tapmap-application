from app.infrastructure.exceptions.geocoder import GeocodingFailed, IncorrectGeolocation

from app.config import settings
from app.services.geocoder.base import BaseGeocoder
from app.services.http_client.base import BaseHttpClient


class Geocoder(BaseGeocoder):
    BASE_URL = settings.geocoder_base__url
    
    def __init__(self, http_client: BaseHttpClient) -> None:
        self.http_client = http_client
    
    async def get_coordinates(self, address: str) -> dict:
        params = {
            "q": address,
            "key": settings.geocoder_api_key,
        }
        data = await self.http_client.get(self.BASE_URL, params=params)
        return self._parse(data)
    
    async def get_address(self, latitude: float, longitude: float) -> dict:
        params = {
            "q": f"{longitude},{latitude}",
            "key": settings.geocoder_api_key,
        }
        data = await self.http_client.get(self.BASE_URL, params=params)
        return self._parse(data)
    
    
    def _parse(self, response: dict) -> dict:
        if response['status']['code'] != 200:
            raise GeocodingFailed(response)
        if response.get("total_results", 0) == 0:
            raise IncorrectGeolocation()

        data = response['results'][0]['components']
        geometry = response['results'][0]['geometry']

        city = data.get('_normalized_city', '')
        road = data.get('road', '')
        house_number = data.get('house_number', '')
        
        address = f"{city}, {road} {house_number}".strip().strip(',')

        return {
            "address": address,
            "coordinates": {"latitude": geometry['lat'], "longitude": geometry['lng']},
            "city": city,
            "state": data.get('state', ''),
        }
