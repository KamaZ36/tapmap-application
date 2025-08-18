from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.user import CurrentUser
from app.application.exceptions.permission import NoAccess

from app.domain.entities.driver import Driver
from app.domain.entities.user import UserRole

from app.infrastructure.repositories.driver.base import BaseDriverRepository


@dataclass
class GetDriverInteraction:
    driver_repository: BaseDriverRepository
      
    async def __call__(self, current_user: CurrentUser, driver_id: UUID) -> Driver:
        self._validate_permissions(current_user=current_user, driver_id=driver_id)
        driver = await self.driver_repository.get_by_id(driver_id)
        return driver
            
    def _validate_permissions(self, current_user: CurrentUser, driver_id: UUID) -> None:
        if current_user.user_id == driver_id:
            return
        if UserRole.admin is current_user.roles:
            return
        raise NoAccess()
    