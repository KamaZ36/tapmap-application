from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand, CommandHandler
from app.application.exceptions.user import UserBlockNotFound
from app.domain.entities.blocking_user import BlockingUser

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.blocking_user.base import (
    BaseBlockingUserRepository,
)


@dataclass(frozen=True, eq=False)
class UnblockUserCommand(BaseCommand):
    current_user_id: UUID
    user_id: UUID


@dataclass(frozen=True, eq=False)
class UnblockUserCommandHandler(CommandHandler[UnblockUserCommand, bool]):
    blocking_user_repository: BaseBlockingUserRepository
    transaction_manager: TransactionManager

    async def __call__(self, command: UnblockUserCommand) -> bool:
        blocking_user = await self.blocking_user_repository.get_active_for_user(
            command.user_id
        )
        if blocking_user is None:
            return True

        blocking_user.unblock()

        await self.blocking_user_repository.update(blocking_user)
        await self.transaction_manager.commit()

        return True
