from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions.draft_order import DraftOrderNotFound
from app.domain.entities.draft_order import DraftOrder
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository


@dataclass
class GetDraftOrderInteraction:
    draft_order_repo: BaseDraftOrderRepository

    async def __call__(self, user_id: UUID) -> DraftOrder | None:
        draft_order = await self.draft_order_repo.get_by_customer_id(user_id)
        if draft_order is None:
            raise DraftOrderNotFound()
        return draft_order
