from dataclasses import dataclass

from app.application.commands.user import CreateUserCommand
from app.domain.entities.user import User
from app.domain.value_objects.phone_number import PhoneNumber

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.unit_of_work.base import BaseUnitOfWork


@dataclass
class CreateUserInteraction:
    user_repository: BaseUserRepository
    transaction_manager: TransactionManager
    
    async def __call__(self, command: CreateUserCommand) -> User:
        phone_number = PhoneNumber(command.phone_number)
        
        user = User(
            name=command.name, 
            phone_number=phone_number
        )
        await self.user_repository.create(user)
        await self.transaction_manager.commit()
        return user
    