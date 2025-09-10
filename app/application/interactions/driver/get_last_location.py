from dataclasses import dataclass
from uuid import UUID

from app.domain.value_objects.coordinates import Coordinates

from app.infrastructure.repositories.driver.base import BaseDriverRepository


@dataclass
class GetLastLocationDriverInteraction:
    driver_repository: BaseDriverRepository

    async def __call__(self, driver_id: UUID) -> Coordinates | None:
        driver = await self.driver_repository.get_by_id(driver_id)
        return driver.last_location
