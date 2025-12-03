from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage

from sqlalchemy.ext.asyncio import AsyncSession

from redis.asyncio import Redis

from dishka import Provider, provide, Scope

from app.core.config import settings
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)
from app.infrastructure.repositories.tg_bot_session.redis_repository import (
    RedisTgBotSessionRepository,
)
from app.infrastructure.repositories.tg_bot_session.repository_with_cache import (
    CachedTgBotSessionRepository,
)
from app.infrastructure.repositories.tg_bot_session.sqlalchemy_repository import (
    SQLTgBotSessionRepository,
)


class UserTgBot(Bot):
    pass


class UserDispatcher(Dispatcher):
    pass


class DriverTgBot(Bot):
    pass


class DriverDispatcher(Dispatcher):
    pass


class TgBotProvider(Provider):
    @provide(scope=Scope.APP)
    def get_user_tg_bot(self) -> UserTgBot:
        bot = UserTgBot(token=settings.user_tg_bot_token)
        return bot

    @provide(scope=Scope.APP)
    def get_user_dispatcher(self, redis: Redis, bot: UserTgBot) -> UserDispatcher:
        redis_storage = RedisStorage(redis)
        return UserDispatcher(bot=bot, storage=redis_storage)

    @provide(scope=Scope.APP)
    def get_driver_tg_bot(self) -> DriverTgBot:
        bot = DriverTgBot(token=settings.driver_tg_bot_token)
        return bot

    @provide(scope=Scope.APP)
    def get_driver_dispatcher(self, redis: Redis, bot: DriverTgBot) -> DriverDispatcher:
        redis_storage = RedisStorage(redis)
        return DriverDispatcher(bot=bot, storage=redis_storage)

    @provide(scope=Scope.REQUEST)
    def get_redis_auth_session_repo(self, redis: Redis) -> RedisTgBotSessionRepository:
        return RedisTgBotSessionRepository(redis)

    @provide(scope=Scope.REQUEST)
    def get_sql_auth_session_repo(
        self, session: AsyncSession
    ) -> SQLTgBotSessionRepository:
        return SQLTgBotSessionRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_cached_auth_session_repo(
        self,
        redis_repo: RedisTgBotSessionRepository,
        sql_repo: SQLTgBotSessionRepository,
    ) -> BaseTgBotSessionRepository:
        return CachedTgBotSessionRepository(redis_repo=redis_repo, sql_repo=sql_repo)
