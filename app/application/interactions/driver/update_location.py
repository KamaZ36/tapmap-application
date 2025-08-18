from dataclasses import dataclass

from app.domain.value_objects.coordinates import Coordinates

from app.application.commands.user import SetBaseUserLocationCommand
from app.application.dtos.user import CurrentUser

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.driver.base import BaseDriverRepository


@dataclass
class UpdateLocationInteraction:
    driver_repository: BaseDriverRepository
    transaction_manager: TransactionManager
    
    async def __call__(self, command: SetBaseUserLocationCommand, current_user: CurrentUser) -> None:
        driver = await self.driver_repository.get_by_id(current_user.user_id)
                    
        coordinates = Coordinates(latitude=command.coordinates[0], longitude=command.coordinates[1])
        driver.update_location(coordinates)
        
        await self.driver_repository.update(driver)
        await self.transaction_manager.commit()
        