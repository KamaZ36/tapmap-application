from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.order import ExtendedOrder
from app.application.dtos.user import CurrentUser

from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.order.base import BaseOrderRepository
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.repositories.vehicle.base import BaseVehicleRepository


@dataclass(frozen=True)
class GetActiveOrderForDriverInteraction:
    order_repository: BaseOrderRepository
    user_repository: BaseUserRepository
    driver_repository: BaseDriverRepository
    vehicle_repository: BaseVehicleRepository
        
    async def __call__(self, current_user: CurrentUser) -> ExtendedOrder:
        driver = None
        vehicle = None
        
        order = await self.order_repository.get_active_for_driver(driver_id=current_user.user_id)
        user = await self.user_repository.get_by_id(order.customer_id)
        
        if order.driver_id:
            driver = await self.driver_repository.get_by_id(order.driver_id)
            vehicle = await self.vehicle_repository.get_by_id(driver.id)
        
        extended_order_dto = ExtendedOrder(
            id=order.id,
            customer=user,
            driver=driver,
            city_id=order.city_id,
            vehicle=vehicle,
            points=order.points,
            status=order.status,
            price=order.price,
            service_commission=order.service_commission,
            travel_time=order.travel_time,
            travel_distance=order.travel_distance,
            feeding_distance=order.feeding_distance,
            feeding_time=order.feeding_time,
            comment=order.comment,
            created_at=order.created_at
        )
        
        return extended_order_dto
    