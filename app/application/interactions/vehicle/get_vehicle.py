from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.user import UserRole
from app.domain.entities.vehicle import Vehicle

from app.application.dtos.user import CurrentUser
from app.application.exceptions.permission import NoAccess
from app.application.exceptions.vehicle import VehicleNotFound

from app.infrastructure.repositories.vehicle.base import BaseVehicleRepository


@dataclass
class GetVehicleInteraction:
    vehicle_repository: BaseVehicleRepository
        
    async def __call__(self, vehicle_id: UUID, current_user: CurrentUser) -> Vehicle:
        vehicle = await self.vehicle_repository.get_by_id(vehicle_id)
        if not vehicle:
            raise VehicleNotFound()
        self._validate_permissions(vehicle, current_user)
        return vehicle
            
    def _validate_permissions(self, vehicle: Vehicle, current_user: CurrentUser) -> None:
        if vehicle.driver_id == current_user.user_id:
            return
        if UserRole.admin in current_user.roles:
            return
        raise NoAccess
    