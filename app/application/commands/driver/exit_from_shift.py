from dataclasses import dataclass
from uuid import UUID

from app.application.commands.converters import convert_driver_entity_to_dto
from app.application.dtos.driver import DriverDTO
from app.domain.entities.driver import Driver

from app.application.commands.base import BaseCommand, CommandHandler
from app.application.exceptions.driver import DriverNotFound

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.driver.base import BaseDriverRepository


@dataclass(frozen=True, eq=False)
class DriverExitFromShiftCommand(BaseCommand):
    current_user_id: UUID
    driver_id: UUID


@dataclass(frozen=True, eq=False)
class DriverExitFromShiftCommandHandler(
    CommandHandler[DriverExitFromShiftCommand, DriverDTO]
):
    driver_repository: BaseDriverRepository
    transaction_manager: TransactionManager

    async def __call__(self, command: DriverExitFromShiftCommand) -> DriverDTO:
        driver = await self.driver_repository.get_by_id(command.driver_id)
        if driver is None:
            raise DriverNotFound()

        driver.end_shift()

        await self.driver_repository.update(driver)
        await self.transaction_manager.commit()

        return convert_driver_entity_to_dto(driver)
