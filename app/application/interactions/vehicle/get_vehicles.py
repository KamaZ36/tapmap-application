from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.user import CurrentUser
from app.application.exceptions.permission import NoAccess
from app.domain.entities.user import UserRole
from app.domain.entities.vehicle import Vehicle

from app.infrastructure.repositories.vehicle.base import BaseVehicleRepository



@dataclass
class GetVehiclesInteraction:
    vehicle_repository: BaseVehicleRepository
        
    async def __call__(self, driver_id: UUID, current_user: CurrentUser) -> list[Vehicle]:
        self._validate_permissions(driver_id, current_user)
        vehicles = await self.vehicle_repository.get_by_driver_id(driver_id=driver_id)
        return vehicles
        
    def _validate_permissions(self, driver_id: UUID, current_user: CurrentUser) -> None:
        if driver_id == current_user.user_id and UserRole.driver in current_user.roles:
            return 
        if UserRole.admin in current_user.roles:
            return
        raise NoAccess
        