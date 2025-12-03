from dataclasses import dataclass
from uuid import UUID

from app.application.commands.converters import convert_driver_entity_to_dto
from app.application.dtos.driver import DriverDTO
from app.domain.entities.driver import Driver
from app.domain.value_objects.coordinates import Coordinates

from app.application.commands.base import BaseCommand, CommandHandler
from app.application.exceptions.driver import DriverNotFound

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.driver.base import BaseDriverRepository


@dataclass(frozen=True, eq=False)
class DriverGoToShiftCommand(BaseCommand):
    driver_id: UUID
    current_user_id: UUID
    location: tuple[float, float]


@dataclass(frozen=True, eq=False)
class DriverGoToShiftCommandHandler(CommandHandler[DriverGoToShiftCommand, DriverDTO]):
    driver_repository: BaseDriverRepository
    transaction_manager: TransactionManager

    async def __call__(self, command: DriverGoToShiftCommand) -> DriverDTO:
        driver = await self.driver_repository.get_by_id(command.driver_id)
        if driver is None:
            raise DriverNotFound()

        coordinates = Coordinates(
            latitude=command.location[0], longitude=command.location[1]
        )

        driver.start_shift()
        driver.update_location(coordinates=coordinates)

        await self.driver_repository.update(driver)
        await self.transaction_manager.commit()

        return convert_driver_entity_to_dto(driver)
