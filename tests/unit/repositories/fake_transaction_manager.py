from app.infrastructure.database.transaction_manager.base import TransactionManager


class FakeTransactionManager(TransactionManager):
    """Fake implementation of TransactionManager for testing purposes."""

    def __init__(self):
        self.committed = False
        self.rolled_back = False

    async def commit(self) -> None:
        """Mark transaction as committed."""
        self.committed = True

    async def rollback(self) -> None:
        """Mark transaction as rolled back."""
        self.rolled_back = True

    async def __aenter__(self):
        """Context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - auto-commit on success, rollback on exception."""
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
