from typing import AsyncGenerator
from dishka import Provider, provide, Scope
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.connection import async_session_maker
from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.database.transaction_manager.sqlalchemy import SQLAlchemyTransactionManager
from app.infrastructure.redis.connection import get_redis_client

from app.services.message_broker.base import BaseMessageBroker
from app.services.message_broker.redis_broker import RedisMessageBroker


class BaseAppProvider(Provider):
    
    # DATABASE
    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_transaction_manager(self, session: AsyncSession) -> TransactionManager:
        return SQLAlchemyTransactionManager(session=session)
        
    # REDIS
    @provide(scope=Scope.APP)
    def get_redis_client(self) -> Redis:
        return get_redis_client()
    
    # MESSAGE BROKER
    @provide(scope=Scope.APP)
    def get_message_broker(self, redis: Redis) -> BaseMessageBroker:
        return RedisMessageBroker(redis=redis)
        # return KafkaMessageBroker(producer=AIOKafkaProducer(
        #     bootstrap_servers=settings.kafka_url
        # ))
