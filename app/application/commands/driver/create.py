from dataclasses import dataclass
from uuid import UUID

from app.application.commands.converters import convert_driver_entity_to_dto
from app.domain.entities.driver import Driver
from app.domain.entities.user import UserRole
from app.domain.value_objects.phone_number import PhoneNumber

from app.application.dtos.driver import DriverDTO
from app.application.commands.base import BaseCommand, CommandHandler
from app.application.exceptions.user import UserNotFound

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.user.base import BaseUserRepository


@dataclass(frozen=True, eq=False, kw_only=True)
class CreateDriverCommand(BaseCommand):
    current_user_id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    middle_name: str | None = None
    license_number: str
    phone_number: str


@dataclass
class CreateDriverCommandHandler(CommandHandler[CreateDriverCommand, DriverDTO]):
    driver_repository: BaseDriverRepository
    user_repository: BaseUserRepository
    transaction_manager: TransactionManager

    async def __call__(self, command: CreateDriverCommand) -> DriverDTO:
        user = await self.user_repository.get_by_id(command.user_id)
        if user is None:
            raise UserNotFound()

        driver = Driver(
            id=user.id,
            first_name=command.first_name,
            last_name=command.last_name,
            middle_name=command.middle_name,
            license_number=command.license_number,
            phone_number=PhoneNumber(command.phone_number),
        )

        user.add_role(UserRole.driver)

        await self.driver_repository.create(driver)
        await self.user_repository.update(user)
        await self.transaction_manager.commit()

        return convert_driver_entity_to_dto(driver)
