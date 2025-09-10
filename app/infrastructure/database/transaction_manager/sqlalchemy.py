from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.transaction_manager.base import TransactionManager


@dataclass
class SQLAlchemyTransactionManager(TransactionManager):
    session: AsyncSession

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def close(self) -> None:
        await self.session.close()
