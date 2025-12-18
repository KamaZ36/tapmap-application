from abc import ABC, abstractmethod

from app.application.dtos.location import GeocodedInfoDTO
from app.domain.value_objects.coordinates import Coordinates


class BaseGeocoderGateway(ABC):
    @abstractmethod
    async def get_coordinates(self, address: str) -> GeocodedInfoDTO | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_address(self, coordinates: Coordinates) -> GeocodedInfoDTO | None:
        raise NotImplementedError()
