from httpx import HTTPError
from app.application.dtos.location import GeocodedInfoDTO
from app.core.config import settings

from app.application.exceptions.geolocation import GeocodingServiceUnavailable

from app.domain.value_objects.coordinates import Coordinates
from app.infrastructure.exceptions.geocoder import (
    GeocodingFailed,
)
from app.infrastructure.services.geocoder.base import BaseGeocoder
from app.infrastructure.services.http_client.base import BaseHttpClient


class Geocoder(BaseGeocoder):
    BASE_URL = settings.geocoder_base__url

    def __init__(self, http_client: BaseHttpClient) -> None:
        self.http_client = http_client

    async def get_coordinates(self, address: str) -> GeocodedInfoDTO | None:
        params = {
            "q": f"Россия, {address}",
            "key": settings.geocoder_api_key,
            "language": "ru",
        }
        try:
            data = await self.http_client.get(self.BASE_URL, params=params)
            return self._parse(data)
        except HTTPError:
            raise GeocodingServiceUnavailable()

    async def get_address(self, coordinates: Coordinates) -> GeocodedInfoDTO | None:
        params = {
            "q": f"{coordinates.latitude},{coordinates.longitude}",
            "key": settings.geocoder_api_key,
            "language": "ru",
        }
        try:
            data = await self.http_client.get(self.BASE_URL, params=params)
            return self._parse(data)
        except HTTPError:
            raise GeocodingServiceUnavailable()

    def _parse(self, response: dict) -> GeocodedInfoDTO | None:
        if response["status"]["code"] != 200:
            raise GeocodingFailed(response)
        if response.get("total_results", 0) == 0:
            return None

        data = response["results"][0]["components"]
        geometry = response["results"][0]["geometry"]

        city = data.get("_normalized_city", "")
        road = data.get("road", "")
        house_number = data.get("house_number", "")

        address = f"{city}, {road} {house_number}".strip().strip(",")

        return GeocodedInfoDTO(
            address=address, coordinates=(geometry["lat"], geometry["lng"])
        )
