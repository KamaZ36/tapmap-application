from dataclasses import dataclass

from app.application.dtos.order import ExtendedOrder
from app.application.dtos.user import CurrentUser
from app.application.exceptions.driver import DriverNotFound
from app.application.exceptions.order import OrderNotFound
from app.application.exceptions.user import UserNotFound
from app.application.exceptions.vehicle import VehicleNotFound

from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.order.base import BaseOrderRepository
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.repositories.vehicle.base import BaseVehicleRepository


@dataclass(frozen=True)
class GetActiveOrderForUserInteraction:
    order_repository: BaseOrderRepository
    user_repository: BaseUserRepository
    driver_repository: BaseDriverRepository
    vehicle_repository: BaseVehicleRepository

    async def __call__(self, current_user: CurrentUser) -> ExtendedOrder | None:
        driver = None
        vehicle = None

        order = await self.order_repository.get_active_for_customer(
            customer_id=current_user.user_id
        )
        if not order:
            raise OrderNotFound()

        user = await self.user_repository.get_by_id(order.customer_id)
        if not user:
            raise UserNotFound()

        if order.driver_id:
            driver = await self.driver_repository.get_by_id(order.driver_id)
            if not driver:
                raise DriverNotFound()

            vehicle = await self.vehicle_repository.get_by_driver_id(driver.id)
            if not vehicle:
                raise VehicleNotFound()

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
            created_at=order.created_at,
        )

        return extended_order_dto
