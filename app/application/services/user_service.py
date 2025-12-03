from dataclasses import dataclass
from uuid import UUID

from app.infrastructure.repositories.blocking_user.base import (
    BaseBlockingUserRepository,
)


@dataclass(frozen=True, eq=False)
class UserService:
    blocking_user_repository: BaseBlockingUserRepository

    async def check_user_blocking(self, user_id: UUID) -> bool:
        blocking_user = await self.blocking_user_repository.get_active_for_user(user_id)
        if blocking_user is None:
            return False
        if blocking_user.is_expired():
            blocking_user.unblock()
            await self.blocking_user_repository.update(blocking_user)
            return False
        return True
