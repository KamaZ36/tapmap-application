from dataclasses import dataclass

from app.domain.entities.user import User
from app.domain.value_objects.phone_number import PhoneNumber

from app.application.dtos.user import UserDTO
from app.application.commands.base import BaseCommand, CommandHandler

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.user.base import BaseUserRepository


@dataclass(frozen=True, eq=False)
class CreateUserCommand(BaseCommand):
    phone_number: str
    name: str


@dataclass(frozen=True, eq=False)
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, UserDTO]):
    user_repository: BaseUserRepository
    transaction_manager: TransactionManager

    async def __call__(self, command: CreateUserCommand) -> UserDTO:
        phone_number = PhoneNumber(command.phone_number)
        user = User(name=command.name, phone_number=phone_number)

        await self.user_repository.create(user)
        await self.transaction_manager.commit()

        return UserDTO.from_entity(user)
