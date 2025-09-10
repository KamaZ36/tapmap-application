from dataclasses import dataclass
from uuid import UUID
from loguru import logger

from app.domain.entities.order import Order
from app.domain.entities.user import UserRole

from app.application.dtos.user import CurrentUser
from app.application.exceptions.order import OrderNotFound
from app.application.exceptions.user import UserNotFound
from app.application.exceptions.permission import NoAccess
from app.application.exceptions.driver import DriverNotFound

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.order.base import BaseOrderRepository
from app.infrastructure.repositories.user.base import BaseUserRepository


@dataclass
class CancelOrderInteraction:
    user_repository: BaseUserRepository
    order_repository: BaseOrderRepository
    driver_repository: BaseDriverRepository
    transaction_manager: TransactionManager

    async def __call__(
        self, current_user: CurrentUser, order_id: UUID, reason: str
    ) -> None:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFound()

        user = await self.user_repository.get_by_id(order.customer_id)
        if not user:
            raise UserNotFound()

        # Проверка прав доступа
        self._validate_permissions(current_user=current_user, order=order)

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
            f"Заказ {order_id} успешно отменен {current_user.user_id}. Причина: {reason}"
        )

    def _validate_permissions(self, current_user: CurrentUser, order: Order) -> None:
        """Проверка прав отмены заказа"""
        if order.customer_id == current_user.user_id:
            return

        if (
            order.driver_id == current_user.user_id
            and UserRole.driver in current_user.roles
        ):
            return

        if UserRole.admin in current_user.roles:
            return

        logger.warning(f"Доступ запрещен для пользователя {current_user.user_id}")
        raise NoAccess()
