from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BIGINT

from app.infrastructure.database.models.base import BaseModel, CreatedAtMixin

from app.bots.user_tg_bot.dtos.auth_session import AuthSession


class TgBotAuthSessionModel(BaseModel, CreatedAtMixin):
    __tablename__ = "tg_bot_sessions"

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    tg_id: Mapped[int] = mapped_column(BIGINT, nullable=False, unique=True)
    user_id: Mapped[UUID] = mapped_column(nullable=False, unique=True)

    def to_dto(self) -> AuthSession:
        return AuthSession(
            id=self.id,
            tg_id=self.tg_id,
            user_id=self.user_id,
            created_at=self.created_at,
        )

    @classmethod
    def from_dto(cls, auth_session: AuthSession) -> "TgBotAuthSessionModel":
        return cls(
            id=auth_session.id,
            tg_id=auth_session.tg_id,
            user_id=auth_session.user_id,
        )
