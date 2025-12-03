from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand, CommandHandler
from app.application.commands.converters import convert_order_entities_to_dto
from app.core.config import settings

from app.application.dtos.order import OrderDTO
from app.application.exceptions.order import OrderNotFound
from app.application.exceptions.user import UserNotFound

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository
from app.infrastructure.repositories.order.base import BaseOrderRepository
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.services.message_broker.base import BaseMessageBroker


@dataclass(frozen=True, eq=False)
class ConfirmOrderCommand(BaseCommand):
    order_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, eq=False)
class ConfirmOrderCommandHandler(CommandHandler[ConfirmOrderCommand, OrderDTO]):
    user_repository: BaseUserRepository
    draft_order_repository: BaseDraftOrderRepository
    order_repository: BaseOrderRepository
    message_broker: BaseMessageBroker
    transaction_manager: TransactionManager

    async def __call__(self, command: ConfirmOrderCommand) -> OrderDTO:
        order = await self.draft_order_repository.get_by_id(command.order_id)
        if order is None:
            raise OrderNotFound()

        user = await self.user_repository.get_by_id(order.customer_id)
        if user is None:
            raise UserNotFound()

        order.confirm()

        await self.order_repository.create(order)
        await self.transaction_manager.commit()
        await self.draft_order_repository.delete(order.id)

        event = {"order_id": str(order.id)}

        await self.message_broker.publish(
            topic=settings.order_confirmed_topic, key=str(order.id), value=event
        )

        return convert_order_entities_to_dto(order=order, customer=user)
