from typing import Protocol

from app.application.dtos.location import GeocodedInfoDTO
from app.domain.value_objects.coordinates import Coordinates


class BaseGeocoder(Protocol):
    async def get_coordinates(self, address: str) -> GeocodedInfoDTO | None: ...

    async def get_address(self, coordinates: Coordinates) -> GeocodedInfoDTO | None: ...
