from decimal import Decimal
from typing import Any
from datetime import datetime

from app.domain.enums.order_status import OrderStatus
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.order_point import OrderPoint

from app.application.dtos.order import OrderDTO
from app.application.dtos.user import UserForOrderDTO

from app.infrastructure.database.models.user import UserModel


def convert_order_to_dto(order_row: dict[str, Any], user_model: UserModel) -> OrderDTO:
    customer_for_order_dto = UserForOrderDTO(
        id=user_model.id, name=user_model.name, phone_number=user_model.phone_number
    )

    return OrderDTO(
        id=order_row["id"],
        customer=customer_for_order_dto,
        driver=None,
        city_id=order_row["city_id"],
        vehicle=None,
        points=[
            OrderPoint(
                address=point["address"],
                coordinates=Coordinates(
                    latitude=point["coordinates"]["latitude"],
                    longitude=point["coordinates"]["longitude"],
                ),
            )
            for point in order_row["points"]
        ],
        status=OrderStatus(order_row["status"]),
        price=Decimal(order_row["price"]) if order_row.get("price") else None,
        service_commission=Decimal(order_row["service_commission"]) if order_row.get("service_commission") else None,
        travel_time=order_row["travel_time"],
        travel_distance=order_row["travel_distance"],
        comment=order_row["comment"],
        created_at=datetime.fromisoformat(order_row["created_at"]) if isinstance(order_row["created_at"], str) else order_row["created_at"],
    )
