from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.connection import async_session_maker

from typing import AsyncGenerator
from dishka import Provider, Scope, provide

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.database.transaction_manager.sqlalchemy import SQLAlchemyTransactionManager


class DatabaseProvider(Provider):
    scope = Scope.REQUEST
    
    @provide
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session

    @provide
    def get_transaction_manager(self, session: AsyncSession) -> TransactionManager:
        return SQLAlchemyTransactionManager(session=session)
