from typing import Protocol

from app.domain.value_objects.coordinates import Coordinates


class BaseRouteService(Protocol):
    async def get_distance_route(self, coordinates_list: list[Coordinates]) -> int: ...

    async def get_time_route(self, distance: int) -> int: ...
