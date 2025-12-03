from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.infrastructure.database.models.tg_bot_session import TgBotAuthSessionModel

from app.bots.user_tg_bot.dtos.auth_session import AuthSession


class SQLTgBotSessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, auth_session: AuthSession) -> None:
        auth_session_model = TgBotAuthSessionModel.from_dto(auth_session=auth_session)
        self._session.add(auth_session_model)
        await self._session.commit()

    async def get_by_tg_id(self, tg_id: int) -> AuthSession | None:
        query = select(TgBotAuthSessionModel).where(
            TgBotAuthSessionModel.tg_id == tg_id
        )
        result = await self._session.execute(query)
        auth_session_model = result.scalar_one_or_none()
        return auth_session_model.to_dto() if auth_session_model else None

    async def get_by_user_id(self, user_id: UUID) -> AuthSession | None:
        query = select(TgBotAuthSessionModel).where(
            TgBotAuthSessionModel.user_id == user_id
        )
        result = await self._session.execute(query)
        auth_session_model = result.scalar_one_or_none()
        return auth_session_model.to_dto() if auth_session_model else None
