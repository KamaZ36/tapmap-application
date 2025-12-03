from dataclasses import dataclass
from uuid import UUID
from loguru import logger

from app.core.config import settings

from app.domain.entities.order import Order, OrderStatus

from app.application.commands.base import BaseCommand, CommandHandler
from app.application.exceptions.driver import DriverNotFound
from app.application.exceptions.order import OrderNotFound


from app.infrastructure.services.message_broker.base import BaseMessageBroker
from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.order.base import BaseOrderRepository
from app.infrastructure.repositories.user.base import BaseUserRepository


@dataclass(frozen=True, eq=False)
class UpdateOrderStatusCommand(BaseCommand):
    current_user_id: UUID
    order_id: UUID


@dataclass
class UpdateOrderStatusCommandHandler(
    CommandHandler[UpdateOrderStatusCommand, OrderStatus]
):
    order_repository: BaseOrderRepository
    driver_repository: BaseDriverRepository
    user_repository: BaseUserRepository
    message_broker: BaseMessageBroker
    transaction_manager: TransactionManager

    async def __call__(self, command: UpdateOrderStatusCommand) -> OrderStatus:
        order = await self.order_repository.get_by_id(order_id=command.order_id)
        if order is None:
            raise OrderNotFound()

        prev_status = order.status
        order.update_status()

        if order.status == OrderStatus.completed:
            await self._process_order_completion(order=order)

        await self.order_repository.update(order)
        await self.transaction_manager.commit()

        logger.info(
            f"Пользователь {command.current_user_id} обновил статус заказа {order.id} с {prev_status.value} на {order.status.value}"
        )

        event = {
            "order_id": str(order.id),
            "customer_id": str(order.customer_id),
            "driver_id": str(order.driver_id),
            "status": order.status,
        }
        await self.message_broker.publish(
            topic=settings.order_status_update_topic, key=str(order.id), value=event
        )
        return order.status

    async def _process_order_completion(self, order: Order) -> None:
        user = await self.user_repository.get_by_id(order.customer_id)
        if user is None:
            raise DriverNotFound()
        driver = await self.driver_repository.get_by_id(driver_id=order.driver_id)
        if driver is None:
            raise DriverNotFound()

        user.complete_order()
        driver.complete_order()

        await self.user_repository.update(user)
        await self.driver_repository.update(driver)
