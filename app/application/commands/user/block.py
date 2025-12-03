from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.application.commands.base import BaseCommand, CommandHandler
from app.domain.entities.blocking_user import BlockingUser

from app.infrastructure.repositories.blocking_user.base import (
    BaseBlockingUserRepository,
)
from app.infrastructure.database.transaction_manager.base import TransactionManager


@dataclass(frozen=True, eq=False)
class BlockUserCommand(BaseCommand):
    current_user_id: UUID
    user_id: UUID
    reason: str
    expires_at: datetime


@dataclass(frozen=True, eq=False)
class BlockUserCommandHandler(CommandHandler[BlockUserCommand, BlockingUser]):
    blocking_user_repository: BaseBlockingUserRepository
    transaction_manager: TransactionManager

    async def __call__(self, command: BlockUserCommand) -> BlockingUser:
        blocking_user = BlockingUser(
            user_id=command.user_id,
            reason=command.reason,
            is_active=True,
            expires_at=command.expires_at,
        )

        await self.blocking_user_repository.create(blocking_user)
        await self.transaction_manager.commit()

        return blocking_user
