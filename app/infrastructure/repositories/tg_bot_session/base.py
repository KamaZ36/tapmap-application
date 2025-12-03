from typing import Protocol
from uuid import UUID

from app.bots.user_tg_bot.dtos.auth_session import AuthSession


class BaseTgBotSessionRepository(Protocol):
    async def create(self, auth_session: AuthSession) -> None: ...

    async def get_by_user_id(self, user_id: UUID) -> AuthSession | None: ...

    async def get_by_tg_id(self, tg_id: int) -> AuthSession | None: ...
