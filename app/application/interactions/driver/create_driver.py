from dataclasses import dataclass

from app.application.commands.driver import CreateDriverCommand
from app.application.dtos.user import CurrentUser
from app.application.exceptions.permission import NoAccess

from app.domain.entities.driver import Driver
from app.domain.entities.user import UserRole
from app.domain.value_objects.phone_number import PhoneNumber

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.user.base import BaseUserRepository


@dataclass
class CreateDriverInteraction:
    driver_repository: BaseDriverRepository
    user_repository: BaseUserRepository
    transaction_manager: TransactionManager

    async def __call__(
        self, command: CreateDriverCommand, current_user: CurrentUser
    ) -> Driver:
        user = await self.user_repository.get_by_id(command.user_id)
        self._validate_permissions(current_user)
        driver = Driver(
            id=user.id,
            first_name=command.first_name,
            last_name=command.last_name,
            middle_name=command.middle_name,
            license_number=command.license_number,
            phone_number=PhoneNumber(command.phone_number),
        )
        user.roles.append(UserRole.driver)
        await self.driver_repository.create(driver)
        await self.user_repository.update(user)
        await self.transaction_manager.commit()
        return driver

    def _validate_permissions(self, current_user: CurrentUser) -> None:
        if UserRole.admin in current_user.roles:
            return
        raise NoAccess()
