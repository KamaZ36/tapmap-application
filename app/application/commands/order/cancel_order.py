from dataclasses import dataclass
from uuid import UUID
from loguru import logger

from app.core.config import settings

from app.domain.enums.order_status import OrderStatus

from app.application.commands.base import BaseCommand, CommandHandler
from app.application.exceptions.order import OrderNotFound
from app.application.exceptions.user import UserNotFound
from app.application.exceptions.driver import DriverNotFound

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository
from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.order.base import BaseOrderRepository
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.services.message_broker.base import BaseMessageBroker


@dataclass(frozen=True, eq=False)
class CancelOrderCommand(BaseCommand):
    current_user_id: UUID
    order_id: UUID
    reason: str | None = None


@dataclass
class CancelOrderCommandHandler(CommandHandler[CancelOrderCommand, bool]):
    user_repository: BaseUserRepository
    draft_order_repository: BaseDraftOrderRepository
    order_repository: BaseOrderRepository
    driver_repository: BaseDriverRepository
    message_broker: BaseMessageBroker
    transaction_manager: TransactionManager

    async def __call__(self, command: CancelOrderCommand) -> bool:
        order = await self.draft_order_repository.get_by_id(command.order_id)
        if order is None:
            order = await self.order_repository.get_by_id(command.order_id)
        if not order:
            raise OrderNotFound()

        user = await self.user_repository.get_by_id(order.customer_id)
        if not user:
            raise UserNotFound()

        if order.status == OrderStatus.draft:
            await self.draft_order_repository.delete(order.id)
            return True
        else:
            order.cancel()
            user.cancel_order()

            await self.order_repository.update(order)
            await self.user_repository.update(user)

            if order.driver_id:
                driver = await self.driver_repository.get_by_id(order.driver_id)
                if not driver:
                    raise DriverNotFound()
                driver.cancel_order()
                await self.driver_repository.update(driver)

        await self.transaction_manager.commit()

        logger.success(
            f"Заказ {command.order_id} успешно отменен {command.current_user_id}. Причина: {command.reason}"
        )

        event = {
            "order_id": str(order.id),
            "customer_id": str(order.customer_id),
            "driver_id": str(order.driver_id) if order.driver_id else None,
            "reason": command.reason,
        }

        await self.message_broker.publish(
            topic=settings.order_cancel_topic, key=str(order.id), value=event
        )

        return True
