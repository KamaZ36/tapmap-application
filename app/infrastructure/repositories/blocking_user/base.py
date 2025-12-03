from typing import Protocol
from uuid import UUID

from app.domain.entities.blocking_user import BlockingUser


class BaseBlockingUserRepository(Protocol):
    async def create(self, blocking_user: BlockingUser) -> None: ...

    async def get_active_for_user(self, user_id: UUID) -> BlockingUser | None: ...

    async def update(self, blocking_user: BlockingUser) -> None: ...
