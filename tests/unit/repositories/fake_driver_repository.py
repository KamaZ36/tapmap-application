import math
from uuid import UUID
from app.domain.entities.driver import Driver
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.repositories.driver.base import BaseDriverRepository


class FakeDriverRepository(BaseDriverRepository):
    
    def __init__(self) -> None:
        self._drivers: dict[UUID, Driver]
        self._drivers_by_phone: dict[str, UUID]
        
    async def create(self, driver: Driver) -> None:
        self._drivers[driver.id] = driver
        self._drivers_by_phone[driver.phone_number.value] = driver.id
    
    async def get_by_id(self, driver_id: UUID) -> Driver | None:
        driver = self._drivers.get(driver_id, None)
        return driver
    
    async def get_by_phone(self, phone_number: PhoneNumber) -> Driver | None:
        driver_id = self._drivers_by_phone.get(phone_number.value)
        if driver_id is None:
            return None
        return await self.get_by_id(driver_id)
    
    async def get_nearest_free(self, coordinates: Coordinates) -> Driver | None:
        free_drivers = [
            d for d in self._drivers.values()
            if not d.on_order and d.on_shift and d.last_location
        ]
        
        if not free_drivers:
            return None
        
        def calculate_distance(driver_coordinates: Coordinates) -> float:
            return math.sqrt(
                (coordinates.latitude - driver_coordinates.latitude)**2 +
                (coordinates.longitude - driver_coordinates.longitude)**2
            )
        
        nearest_driver = min(
            free_drivers,
            key=lambda d: calculate_distance(d.last_location),
            default=None
        )
    
        return nearest_driver if nearest_driver else None
    
    async def update(self, driver: Driver) -> None:
        self._drivers[driver.id] = driver
    