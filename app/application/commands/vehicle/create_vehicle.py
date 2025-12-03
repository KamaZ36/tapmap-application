from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.user import UserRole
from app.domain.entities.vehicle import Vehicle
from app.domain.value_objects.vehicle_number import VehicleNumber

from app.application.commands.base import BaseCommand
from app.application.exceptions.driver import DriverNotFound
from app.application.exceptions.permission import NoAccess
from app.application.dtos.user import CurrentUser

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.vehicle.base import BaseVehicleRepository


@dataclass(frozen=True, eq=False)
class CreateVehcielCommand(BaseCommand):
    driver_id: UUID
    brand: str
    model: str
    color: str
    number: str


@dataclass
class CreateVehicleInteraction:
    vehicle_repository: BaseVehicleRepository
    driver_repository: BaseDriverRepository
    transaction_manager: TransactionManager

    async def __call__(
        self, command: CreateVehcielCommand, current_user: CurrentUser
    ) -> Vehicle:
        self._validate_permissions(command, current_user)

        driver = await self.driver_repository.get_by_id(command.driver_id)
        if not driver:
            raise DriverNotFound()

        vehicle = Vehicle(
            driver_id=command.driver_id,
            brand=command.brand,
            model=command.model,
            color=command.color,
            number=VehicleNumber(command.number),
        )

        await self.vehicle_repository.create(vehicle)
        await self.transaction_manager.commit()
        return vehicle

    def _validate_permissions(
        self, data: CreateVehcielCommand, current_user: CurrentUser
    ) -> None:
        if (
            data.driver_id == current_user.user_id
            and UserRole.driver in current_user.roles
        ):
            return
        if UserRole.admin in current_user.roles:
            return

        raise NoAccess()
