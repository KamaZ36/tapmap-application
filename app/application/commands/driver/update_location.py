from dataclasses import dataclass
from uuid import UUID

from app.domain.value_objects.coordinates import Coordinates

from app.application.commands.base import BaseCommand, CommandHandler

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.driver.base import BaseDriverRepository


@dataclass(frozen=True, eq=False)
class UpdateDriverLocationCommand(BaseCommand):
    current_user_id: UUID
    driver_id: UUID
    location: tuple[float, float]


@dataclass(frozen=True, eq=False)
class UpdateDriverLocationCommandHandler(
    CommandHandler[UpdateDriverLocationCommand, None]
):
    driver_repository: BaseDriverRepository
    transaction_manager: TransactionManager

    async def __call__(self, command: UpdateDriverLocationCommand) -> None:
        driver = await self.driver_repository.get_by_id(command.driver_id)
        if driver is None:
            return

        coordinates = Coordinates(
            latitude=command.location[0], longitude=command.location[1]
        )

        driver.update_location(coordinates)

        await self.driver_repository.update(driver)
        await self.transaction_manager.commit()
