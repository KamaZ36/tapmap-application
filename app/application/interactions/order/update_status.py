from dataclasses import dataclass
from uuid import UUID
from loguru import logger
from app.application.exceptions.order import OrderNotFound
from app.settings import settings

from app.domain.entities.order import Order, OrderStatus
from app.domain.entities.user import UserRole

from app.application.commands.order import UpdateOrderStatusCommand
from app.application.dtos.user import CurrentUser
from app.application.exceptions.permission import NoAccess

from app.infrastructure.services.message_broker.base import BaseMessageBroker
from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.order.base import BaseOrderRepository
from app.infrastructure.repositories.user.base import BaseUserRepository


@dataclass
class UpdateStatusInteraction:
    order_repository: BaseOrderRepository
    driver_repository: BaseDriverRepository
    user_repository: BaseUserRepository
    message_broker: BaseMessageBroker
    transaction_manager: TransactionManager

    async def __call__(
        self, current_user: CurrentUser, command: UpdateOrderStatusCommand
    ) -> OrderStatus:
        """Обновление статуса заказа с проверкой прав"""
        order = await self.order_repository.get_by_id(order_id=command.order_id)
        if order is None:
            raise OrderNotFound()

        self._validate_permissions(current_user=current_user, order=order)

        prev_status = order.status
        order.update_status()

        if order.status == OrderStatus.completed:
            await self._process_order_completion(
                driver_repository=self.driver_repository,
                user_repository=self.user_repository,
                order=order,
            )

        await self.order_repository.update(order)
        await self.transaction_manager.commit()

        logger.info(
            f"Пользователь {current_user.user_id} обновил статус заказа {order.id} с {prev_status.value} на {order.status.value}"
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

    async def _process_order_completion(
        self,
        driver_repository: BaseDriverRepository,
        user_repository: BaseUserRepository,
        order: Order,
    ) -> None:
        user = await user_repository.get_by_id(order.customer_id)

        driver = await driver_repository.get_by_id(driver_id=order.driver_id)

        user.complete_order()
        driver.complete_order()

        await user_repository.update(user)
        await driver_repository.update(driver)

    def _validate_permissions(self, current_user: CurrentUser, order: Order) -> None:
        if (
            order.driver_id == current_user.user_id
            and UserRole.driver in current_user.roles
        ):
            return

        if UserRole.admin in current_user.roles:
            return

        raise NoAccess()
