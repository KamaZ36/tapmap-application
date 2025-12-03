from redis.asyncio import Redis

from sqlalchemy.ext.asyncio import AsyncSession

from dishka import Provider, provide, Scope

from app.infrastructure.readers.draft_order.base import BaseDraftOrderReader
from app.infrastructure.readers.draft_order.reader import DraftOrderReader
from app.infrastructure.readers.driver.base import BaseDriverReader
from app.infrastructure.readers.driver.reader import DriverReader
from app.infrastructure.readers.order.base import BaseOrderReader
from app.infrastructure.readers.order.sql_reader import SQLOrderReader
from app.infrastructure.readers.user.base import BaseUserReader
from app.infrastructure.readers.user.sql_reader import SQLUserReader


class ReadersProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_draft_order_reader(
        self, redis: Redis, session: AsyncSession
    ) -> BaseDraftOrderReader:
        return DraftOrderReader(redis=redis, session=session)

    @provide
    def get_order_reader(self, session: AsyncSession) -> BaseOrderReader:
        return SQLOrderReader(session)

    @provide
    def get_user_reader(self, session: AsyncSession) -> BaseUserReader:
        return SQLUserReader(session)

    @provide
    def get_driver_reader(self, session: AsyncSession) -> BaseDriverReader:
        return DriverReader(session=session)
