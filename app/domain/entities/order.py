from dataclasses import dataclass, field
from uuid import UUID

from app.domain.enums.order_status import OrderStatus
from app.domain.events.order import OrderConfirmed
from app.domain.exceptions.draft_order import (
    ConsecutiveDuplicatePointError,
    InvalidRoutePointIndexError,
)
from app.utils.uuid_v7 import uuid7
from app.domain.entities.base import Entity
from app.domain.exceptions.order import (
    DriverAlreadyAssignedToOrder,
    InvalidOrderStatusTransition,
    OrderCannotBeConfirmedWithoutPriceError,
    OrderCannotTwoPoints,
)
from app.domain.value_objects.order_comment import OrderComment
from app.domain.value_objects.money import Money
from app.domain.value_objects.order_point import OrderPoint


STATUS_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.driver_search: {OrderStatus.waiting_driver, OrderStatus.cancelled},
    OrderStatus.waiting_driver: {
        OrderStatus.driver_waiting_customer,
        OrderStatus.cancelled,
    },
    OrderStatus.driver_waiting_customer: {
        OrderStatus.processing,
        OrderStatus.cancelled,
    },
    OrderStatus.processing: {OrderStatus.completed, OrderStatus.cancelled},
    OrderStatus.completed: set(),
    OrderStatus.cancelled: set(),
}


@dataclass(kw_only=True)
class Order(Entity):
    customer_id: UUID = field(default_factory=uuid7)
    driver_id: UUID | None = None
    city_id: UUID

    points: list[OrderPoint]
    status: OrderStatus = OrderStatus.draft

    price: Money | None
    service_commission: Money | None

    travel_distance: int | None  # В метрах
    travel_time: int | None  # В минутах

    feeding_distance: int | None = None  # В метрах
    feeding_time: int | None = None  # В минутах

    comment: OrderComment | None = field(default=None)

    def add_point(
        self,
        point: OrderPoint,
        price: Money,
        service_commission: Money,
        travel_time: int,
        travel_distance: int,
    ) -> None:
        """Добавить точку маршрута в маршрут заказа

        Args:
            point (Point): Точка для добавления
            price (Money): Пересчитанная цена
            service_commission (Money): Пересчитанная комиссия сервиса

        Raises:
            ConsecutiveDuplicatePointError: Точка совпадает с предыдущей
        """
        if self.points[-1] == point:
            raise ConsecutiveDuplicatePointError(
                new_point=point, prev_point=self.points[-1]
            )
        self.points.append(point)
        self.service_commission = service_commission
        self._update_price(price=price)
        self._update_route_info(
            travel_time=travel_time, travel_distance=travel_distance
        )

    def delete_point(self, index: int, price: Money) -> None:
        """Удалить точку маршрута из маршрута заказа

        Args:
            index (int): Индекс точки в списке маршрута
            price (Money): Пересчитанная цена
            service_commission (Money): Пересчитанная комиссия сервиса

        Raises:
            InvalidRoutePointIndexError: Индекс меньше нуля или больше списка маршрута
        """
        if index < 0 or index >= len(self.points):
            raise InvalidRoutePointIndexError(index=index, route_len=len(self.points))
        del self.points[index]
        self._update_price(price=price)

    def change_status(self, status: OrderStatus) -> None:
        """_summary_

        Args:
            status (OrderStatus): Новый статус

        Raises:
            InvalidOrderStatusTransition: Некорректное переключение статуса
        """
        if status not in STATUS_TRANSITIONS.get(self.status, set()):
            raise InvalidOrderStatusTransition(self.status, status)
        if status == OrderStatus.waiting_driver and self.driver_id is None:
            raise InvalidOrderStatusTransition(self.status, status)
        self.status = status

    def assign_driver(
        self, driver_id: UUID, feeding_time: int, feeding_distance: int
    ) -> None:
        """Назначить водителя на заказ

        Args:
            driver_id (UUID): Идентификатор водителя

        Raises:
            DriverAlreadyAssigned: Водитель уже назначен
        """
        if self.driver_id is not None:
            raise DriverAlreadyAssignedToOrder(
                order_id=self.id, assigned_driver=self.driver_id
            )
        self.driver_id = driver_id
        self.feeding_distance = feeding_distance
        self.feeding_time = feeding_time
        self.change_status(status=OrderStatus.waiting_driver)

    def update_status(self) -> None:
        next_status = self._get_next_status()
        if next_status is None:
            raise InvalidOrderStatusTransition(self.status, next_status)
        self.change_status(status=next_status)

    def add_comment(self, comment: OrderComment) -> None:
        self.comment = comment

    def confirm(self) -> None:
        if len(self.points) < 2:
            raise OrderCannotTwoPoints()
        if self.price is None or self.service_commission is None:
            raise OrderCannotBeConfirmedWithoutPriceError()
        self.status = OrderStatus.driver_search
        self._events.append(OrderConfirmed(order_id=self.id))

    def cancel(self) -> None:
        self.change_status(status=OrderStatus.cancelled)

    def _get_next_status(self) -> OrderStatus | None:
        status_rules = {
            OrderStatus.driver_search: OrderStatus.waiting_driver,
            OrderStatus.waiting_driver: OrderStatus.driver_waiting_customer,
            OrderStatus.driver_waiting_customer: OrderStatus.processing,
            OrderStatus.processing: OrderStatus.completed,
            OrderStatus.completed: None,
            OrderStatus.cancelled: None,
        }
        return status_rules[self.status]

    def _update_price(self, price: Money) -> None:
        self.price = price

    def _update_route_info(self, travel_time: int, travel_distance: int) -> None:
        self.travel_distance = travel_distance
        self.travel_time = travel_time
