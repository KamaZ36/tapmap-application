from typing import Protocol
from uuid import UUID

from app.application.exceptions.driver import DriverNotFound
from app.domain.entities.driver import Driver
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.phone_number import PhoneNumber


class BaseDriverRepository(Protocol):
    async def create(self, driver: Driver) -> None: ...

    async def get_by_id(self, driver_id: UUID) -> Driver | None: ...

    async def try_get_by_id(self, driver_id: UUID) -> Driver | DriverNotFound: ...

    async def get_by_phone(self, phone_number: PhoneNumber) -> Driver | None: ...

    async def get_nearest_free(self, coordinates: Coordinates) -> Driver | None: ...

    async def update(self, driver: Driver) -> None: ...
