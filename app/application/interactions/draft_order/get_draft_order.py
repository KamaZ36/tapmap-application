from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.draft_order import DraftOrder
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository


@dataclass
class GetDraftOrderInteraction:
    draft_order_repo: BaseDraftOrderRepository
        
    async def __call__(self, user_id: UUID) -> DraftOrder:
        draft_order = await self.draft_order_repo.get_by_customer_id(user_id)
        return draft_order
    