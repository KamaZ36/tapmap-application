from app.application.dtos.city import CityDTO
from app.application.dtos.driver import DriverDTO, DriverForOrderDTO
from app.application.dtos.order import OrderDTO
from app.application.dtos.user import UserForOrderDTO
from app.domain.entities.city import City
from app.domain.entities.driver import Driver
from app.domain.entities.order import Order
from app.domain.entities.user import User
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.order_point import OrderPoint


def convert_user_entity_to_dto_for_order(user: User) -> UserForOrderDTO:
    return UserForOrderDTO(
        id=user.id, name=user.name, phone_number=user.phone_number.value
    )


def convert_driver_entity_to_dto_for_order(driver: Driver) -> DriverForOrderDTO:
    return DriverForOrderDTO(
        id=driver.id,
        first_name=driver.first_name,
        middle_name=driver.middle_name,
        phone_number=driver.phone_number.value,
    )


def convert_order_entities_to_dto(
    order: Order, customer: User, driver: Driver | None = None
) -> OrderDTO:
    driver_for_order = None

    user_for_order = convert_user_entity_to_dto_for_order(customer)
    if driver:
        driver_for_order = convert_driver_entity_to_dto_for_order(driver)

    price = order.price.value if order.price else None
    service_commission = (
        order.service_commission.value if order.service_commission else None
    )
    comment = order.comment.text if order.comment else None

    return OrderDTO(
        id=order.id,
        customer=user_for_order,
        driver=driver_for_order,
        vehicle=None,
        city_id=order.city_id,
        points=order.points,
        status=order.status,
        price=price,
        service_commission=service_commission,
        travel_distance=order.travel_distance,
        travel_time=order.travel_time,
        feeding_distance=order.feeding_distance,
        feeding_time=order.feeding_time,
        comment=comment,
        created_at=order.created_at,
    )


def convert_driver_entity_to_dto(driver: Driver) -> DriverDTO:
    return DriverDTO(
        id=driver.id,
        first_name=driver.first_name,
        last_name=driver.last_name,
        middle_name=driver.middle_name,
        phone_number=driver.phone_number.value,
        license_number=driver.license_number,
        completed_orders_count=driver.completed_orders_count,
        cancelled_orders_count=driver.cancelled_orders_count,
        status=driver.status,
        on_shift=driver.on_shift,
        on_order=driver.on_order,
        created_at=driver.created_at,
    )


def convert_city_entity_to_dto(city: City) -> CityDTO:
    return CityDTO(
        id=city.id,
        name=city.name,
        state=city.state,
        base_price=city.base_price,
        price_per_kilometer=city.price_per_kilometer,
        service_commission_pct=city.service_commission_pct,
        polygon=city.polygon,
    )
