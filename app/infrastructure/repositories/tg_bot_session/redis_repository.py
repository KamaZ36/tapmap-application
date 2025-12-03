from datetime import datetime
from uuid import UUID
import orjson
from redis.asyncio import Redis

from app.bots.user_tg_bot.dtos.auth_session import AuthSession
from app.bots.user_tg_bot.exceptions.auth_session import AuthSessionNotFound


class RedisTgBotSessionRepository:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def _make_tg_id_key(self, tg_id: int) -> str:
        return f"auth_session:tg_id:{tg_id}"

    def _make_user_id_key(self, user_id: UUID) -> str:
        return f"auth_session:user_id:{str(user_id)}"

    async def create(self, auth_session: AuthSession) -> None:
        auth_session_key = self._make_tg_id_key(auth_session.tg_id)
        user_id_key = self._make_user_id_key(auth_session.user_id)

        auth_session_raw = orjson.dumps(self._to_dict(auth_session))

        async with self._redis.pipeline() as pipe:
            await pipe.set(auth_session_key, auth_session_raw)
            await pipe.set(user_id_key, str(auth_session.tg_id))
            await pipe.execute()

    async def get_by_tg_id(self, tg_id: int) -> AuthSession | None:
        auth_session_key = self._make_tg_id_key(tg_id=tg_id)
        auth_session_raw = await self._redis.get(auth_session_key)
        if auth_session_raw is None:
            return None
        return self._to_dto(auth_session_raw)

    async def get_by_user_id(self, user_id: UUID) -> AuthSession | None:
        user_id_key = self._make_user_id_key(user_id)
        tg_id_raw = await self._redis.get(user_id_key)
        if not tg_id_raw:
            return None
        try:
            tg_id = int(tg_id_raw.decode("utf-8"))
            return await self.get_by_tg_id(tg_id)
        except (ValueError, AttributeError, UnicodeDecodeError):
            return None

    def _to_dict(self, auth_session: AuthSession) -> dict:
        return {
            "id": str(auth_session.id),
            "user_id": str(auth_session.user_id),
            "tg_id": auth_session.tg_id,
            "created_at": auth_session.created_at.isoformat(),
        }

    def _to_dto(self, data: bytes) -> AuthSession:
        raw = orjson.loads(data)
        return AuthSession(
            id=UUID(raw["id"]),
            tg_id=raw["tg_id"],
            user_id=UUID(raw["user_id"]),
            created_at=datetime.fromisoformat(raw["created_at"]),
        )
