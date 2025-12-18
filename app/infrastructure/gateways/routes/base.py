from abc import ABC, abstractmethod

from app.domain.value_objects.coordinates import Coordinates


class BaseRouteInfoGateway(ABC):
    @abstractmethod
    async def get_distance_route(self, coordinates_list: list[Coordinates]) -> int:
        raise NotImplementedError()
