from dataclasses import dataclass
from uuid import UUID

from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository


@dataclass
class DeleteDraftOrderInteraction:
    draft_order_repo: BaseDraftOrderRepository

    async def __call__(self, user_id: UUID) -> None:
        await self.draft_order_repo.delete(user_id)
