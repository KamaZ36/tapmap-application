import asyncio

from uuid import UUID

from app.bots.user_tg_bot.dtos.auth_session import AuthSession

from app.bots.user_tg_bot.exceptions.auth_session import AuthSessionNotFound
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)
from app.infrastructure.repositories.tg_bot_session.redis_repository import (
    RedisTgBotSessionRepository,
)
from app.infrastructure.repositories.tg_bot_session.sqlalchemy_repository import (
    SQLTgBotSessionRepository,
)


class CachedTgBotSessionRepository(BaseTgBotSessionRepository):
    def __init__(
        self,
        redis_repo: RedisTgBotSessionRepository,
        sql_repo: SQLTgBotSessionRepository,
    ) -> None:
        self._redis_repo = redis_repo
        self._sql_repo = sql_repo

    async def create(self, auth_session: AuthSession) -> None:
        await self._sql_repo.create(auth_session)
        await self._redis_repo.create(auth_session)

    async def get_by_tg_id(self, tg_id: int) -> AuthSession | None:
        auth_session = await self._redis_repo.get_by_tg_id(tg_id)
        if auth_session:
            return auth_session
        auth_session = await self._sql_repo.get_by_tg_id(tg_id)
        if auth_session is None:
            return None
        asyncio.create_task(self._redis_repo.create(auth_session))
        return auth_session

    async def get_by_user_id(self, user_id: UUID) -> AuthSession | None:
        auth_session = await self._redis_repo.get_by_user_id(user_id)
        if auth_session:
            return auth_session

        auth_session = await self._sql_repo.get_by_user_id(user_id)
        if auth_session is None:
            return None
        asyncio.create_task(self._redis_repo.create(auth_session))
        return auth_session
