from dataclasses import dataclass
from uuid import UUID
from loguru import logger

from app.domain.entities.order import Order

from app.application.exceptions.draft_order import DraftOrderNotFound
from app.application.services.pricing.pricing_service import PricingService

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.city.base import BaseCityRepository
from app.infrastructure.repositories.order.base import BaseOrderRepository
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository
from app.infrastructure.services.message_broker.base import BaseMessageBroker


@dataclass
class ConfirmDraftOrderInteraction:
    city_repository: BaseCityRepository
    order_repository: BaseOrderRepository
    draft_order_repo: BaseDraftOrderRepository
    pricing_service: PricingService
    message_broker: BaseMessageBroker
    transaction_manager: TransactionManager

    async def __call__(self, user_id: UUID) -> Order:
        draft_order = await self.draft_order_repo.get_by_customer_id(user_id)
        if not draft_order:
            raise DraftOrderNotFound()

        city = await self.city_repository.get_by_id(draft_order.city_id)

        service_commission = self.pricing_service.calculate_commission(
            city=city, price=draft_order.price
        )

        order = Order(
            id=draft_order.id,
            customer_id=draft_order.customer_id,
            city_id=draft_order.city_id,
            points=draft_order.points,
            price=draft_order.price,
            service_commission=service_commission,
            travel_distance=draft_order.travel_distance,
            travel_time=draft_order.travel_time,
            comment=draft_order.comment,
        )
        await self.order_repository.create(order)
        await self.draft_order_repo.delete(user_id)

        await self.transaction_manager.commit()

        logger.success(f"Пользователь {user_id} подтвердил заказ {order.id}")

        return order
