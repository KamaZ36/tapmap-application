from typing import Protocol

from app.domain.value_objects.coordinates import Coordinates


class BaseRouter(Protocol):
    async def get_distance_route(self, coordinates_list: list[Coordinates]) -> int: ...
