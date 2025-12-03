from dataclasses import dataclass
from uuid import UUID

from app.application.commands.converters import convert_order_entities_to_dto
from app.domain.value_objects.order_comment import OrderComment

from app.application.commands.base import BaseCommand, CommandHandler
from app.application.dtos.order import OrderDTO
from app.application.exceptions.user import UserNotFound
from app.application.exceptions.order import OrderNotFound

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository
from app.infrastructure.repositories.user.base import BaseUserRepository


@dataclass(frozen=True, eq=False)
class AddCommentToOrderCommand(BaseCommand):
    current_user_id: UUID
    order_id: UUID
    comment: str


@dataclass(frozen=True, eq=False)
class AddCommentToOrderCommandHandler(
    CommandHandler[AddCommentToOrderCommand, OrderDTO]
):
    user_repository: BaseUserRepository
    draft_order_repository: BaseDraftOrderRepository
    transaction_manager: TransactionManager

    async def __call__(self, command: AddCommentToOrderCommand) -> OrderDTO:
        comment = OrderComment(command.comment)

        order = await self.draft_order_repository.get_by_id(command.order_id)
        if order is None:
            raise OrderNotFound()

        user = await self.user_repository.get_by_id(order.customer_id)
        if user is None:
            raise UserNotFound

        order.add_comment(comment=comment)

        await self.draft_order_repository.update(order)

        return convert_order_entities_to_dto(order=order, customer=user)
