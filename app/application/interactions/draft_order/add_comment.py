from dataclasses import dataclass
from uuid import UUID

from app.application.commands.order import AddCommentToDraftOrderCommand
from app.application.exceptions.draft_order import DraftOrderNotFound

from app.domain.entities.draft_order import DraftOrder
from app.domain.value_objects.order_comment import OrderComment

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository


@dataclass
class AddCommentToDraftOrderInteraction:
    draft_order_repo: BaseDraftOrderRepository

    async def __call__(self, user_id: UUID, command: AddCommentToDraftOrderCommand) -> DraftOrder:
        comment = OrderComment(command.comment)
        draft_order = await self.draft_order_repo.get_by_customer_id(user_id)
        if not draft_order:
            raise DraftOrderNotFound()
        draft_order.add_comment(comment)
        await self.draft_order_repo.update(draft_order)
        return draft_order
    