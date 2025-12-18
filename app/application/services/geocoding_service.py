from app.application.dtos.location import GeocodedInfoDTO
from app.domain.value_objects.coordinates import Coordinates
from app.infrastructure.gateways.geocoder.base import BaseGeocoderGateway


class GeocodingService:
    def __init__(self, geocoder_gateway: BaseGeocoderGateway) -> None:
        self.geocoder_gateway = geocoder_gateway

    async def get_coordinates(self, address: str) -> GeocodedInfoDTO:
        data = await self.geocoder_gateway.get_coordinates(address=address)
        return data

    async def get_address(self, coordinates: Coordinates) -> GeocodedInfoDTO:
        data = await self.geocoder_gateway.get_coordinates(coordinates=coordinates)
        return data
