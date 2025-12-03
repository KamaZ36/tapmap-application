from decimal import Decimal

from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.order_point import OrderPoint

from app.application.dtos.driver import DriverForOrderDTO
from app.application.dtos.order import OrderDTO, OrderForListDTO
from app.application.dtos.user import UserForOrderDTO

from app.infrastructure.database.models.order import OrderModel


def convert_order_to_dto(
    order_model: OrderModel,
) -> OrderDTO:
    driver_for_order_dto = None
    vehicle_for_order_dto = None
    customer_for_order_dto = UserForOrderDTO(
        id=order_model.customer.id,
        name=order_model.customer.name,
        phone_number=order_model.customer.phone_number,
    )

    if order_model.driver:
        driver_for_order_dto = DriverForOrderDTO(
            id=order_model.driver.id,
            first_name=order_model.driver.first_name,
            middle_name=order_model.driver.middle_name,
            phone_number=order_model.driver.phone_number,
        )

    price = str(order_model.price)
    service_commission = str(order_model.service_commission)

    return OrderDTO(
        id=order_model.id,
        customer=customer_for_order_dto,
        driver=driver_for_order_dto,
        city_id=order_model.city_id,
        vehicle=vehicle_for_order_dto,
        points=[
            OrderPoint(
                address=point["address"],
                coordinates=Coordinates(
                    latitude=point["coordinates"]["latitude"],
                    longitude=point["coordinates"]["longitude"],
                ),
            )
            for point in order_model.points
        ],
        status=order_model.status,
        price=Decimal(price),
        service_commission=Decimal(service_commission),
        travel_time=order_model.travel_time,
        travel_distance=order_model.travel_distance,
        feeding_distance=order_model.feeding_distance,
        feeding_time=order_model.feeding_time,
        comment=order_model.comment,
        created_at=order_model.created_at,
    )


def convert_order_to_order_for_list(order: OrderModel) -> OrderForListDTO:
    return OrderForListDTO(id=order.id, created_at=order.created_at)
