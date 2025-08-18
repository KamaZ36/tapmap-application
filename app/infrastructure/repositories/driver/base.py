from typing import Protocol
from uuid import UUID

from app.domain.entities.driver import Driver
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.phone_number import PhoneNumber
from app.domain.value_objects.point import Point


class BaseDriverRepository(Protocol): 
    
    async def create(self, driver: Driver) -> None: ...
    
    async def get_by_id(self, driver_id: UUID) -> Driver: ...

    async def get_by_phone(self, phone_number: PhoneNumber) -> Driver: ...

    async def get_nearest_free(self, coordinates: Coordinates) -> Driver | None: ...

    async def update(self, driver: Driver) -> None: ...
