from typing import Protocol
from uuid import UUID

from app.domain.entities.city import City
from app.domain.value_objects.coordinates import Coordinates


class BaseCityRepository(Protocol):
    async def create(self, city: City) -> None: ...

    async def get_by_id(self, city_id: UUID) -> City | None: ...

    async def try_get_by_id(self, city_id: UUID) -> City | None: ...

    async def get_by_into_point(self, coordinates: Coordinates) -> City | None: ...

    async def update(self, city: City) -> None: ...
