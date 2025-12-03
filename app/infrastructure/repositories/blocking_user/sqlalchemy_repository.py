from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.domain.entities.blocking_user import BlockingUser

from app.infrastructure.database.models.user import BlockingUserModel
from app.infrastructure.repositories.blocking_user.base import (
    BaseBlockingUserRepository,
)


class SQLBlockingUserRepository(BaseBlockingUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, blocking_user: BlockingUser) -> None:
        blocking_user_model = BlockingUserModel.from_entity(blocking_user)
        self._session.add(blocking_user_model)

    async def get_active_for_user(self, user_id: UUID) -> BlockingUser | None:
        query = select(BlockingUserModel).where(
            BlockingUserModel.user_id == user_id, BlockingUserModel.is_active
        )
        result = await self._session.execute(query)
        blocking_user_model = result.scalar_one_or_none()
        return blocking_user_model.to_entity() if blocking_user_model else None

    async def update(self, blocking_user: BlockingUser) -> None:
        stmt = (
            update(BlockingUserModel)
            .where(BlockingUserModel.id == blocking_user.id)
            .values(is_active=blocking_user.is_active)
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(stmt)
