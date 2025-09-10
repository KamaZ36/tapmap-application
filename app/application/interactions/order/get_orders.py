from dataclasses import dataclass

from app.application.dtos.user import CurrentUser
from app.domain.entities.order import Order
from app.domain.entities.user import UserRole

from app.application.exceptions.permission import NoAccess

from app.infrastructure.repositories.order.base import BaseOrderRepository

from app.application.dtos.order import GetOrdersFilters


@dataclass
class GetOrdersInteraction:
    order_repository: BaseOrderRepository

    async def __call__(
        self, filters: GetOrdersFilters, current_user: CurrentUser
    ) -> list[Order]:
        self._validate_permissions(current_user=current_user, filters=filters)

        orders = await self.order_repository.get_filtered_orders(filters)
        return orders

    def _validate_permissions(
        self, current_user: CurrentUser, filters: GetOrdersFilters
    ) -> None:
        if current_user.user_id == filters.customer_id:
            return
        if current_user.user_id == filters.driver_id:
            return
        if UserRole.admin in current_user.roles:
            return

        raise NoAccess()
