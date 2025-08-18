from dataclasses import dataclass, field
from uuid import UUID

from app.domain.enums.order_status import OrderStatus
from app.domain.utils.uuid_v7 import uuid7
from app.domain.entities.base import Entity
from app.domain.exceptions.order import DriverAlreadyAssignedToOrder, InvalidOrderStatusTransition, OrderCannotTwoPoints
from app.domain.value_objects.order_comment import OrderComment
from app.domain.value_objects.money import Money
from app.domain.value_objects.point import Point


STATUS_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.driver_search: {OrderStatus.waiting_driver, OrderStatus.cancelled},
    OrderStatus.waiting_driver: {OrderStatus.driver_waiting_customer, OrderStatus.cancelled},
    OrderStatus.driver_waiting_customer: {OrderStatus.processing, OrderStatus.cancelled},
    OrderStatus.processing: {OrderStatus.completed, OrderStatus.cancelled},
    OrderStatus.completed: set(),
    OrderStatus.cancelled: set()
}

@dataclass(kw_only=True)
class Order(Entity): 
    customer_id: UUID = field(default_factory=uuid7)
    driver_id: UUID | None = None
    city_id: UUID
    
    points: list[Point]
    status: OrderStatus = OrderStatus.driver_search
    
    price: Money
    service_commission: Money
    
    travel_distance: int # В метрах
    travel_time: int # В минутах
    
    feeding_distance: int | None = None # В метрах
    feeding_time: int | None = None # В минутах

    comment: OrderComment | None = field(default=None)

    def __post_init__(self) -> None: 
        if len(self.points) < 2: 
            raise OrderCannotTwoPoints()
        
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

    def assign_driver(self, driver_id: UUID, feeding_time: int, feeding_distance: int) -> None: 
        """Назначить водителя на заказ

        Args:
            driver_id (UUID): Идентификатор водителя

        Raises:
            DriverAlreadyAssigned: Водитель уже назначен
        """
        if self.driver_id is not None:
            raise DriverAlreadyAssignedToOrder(order_id=self.id, assigned_driver=self.driver_id)
        self.driver_id = driver_id
        self.feeding_distance=feeding_distance
        self.feeding_time=feeding_time
        self.change_status(status=OrderStatus.waiting_driver)
        
    def update_status(self) -> None:
        next_status = self._get_next_status()
        if next_status is None:
            raise InvalidOrderStatusTransition(self.status, next_status)
        self.change_status(status=next_status)  
    
    def cancel(self) -> None: 
        self.change_status(status=OrderStatus.cancelled)
        
    def _get_next_status(self) -> OrderStatus | None:
        status_rules = {
            OrderStatus.driver_search: OrderStatus.waiting_driver,
            OrderStatus.waiting_driver: OrderStatus.driver_waiting_customer,
            OrderStatus.driver_waiting_customer: OrderStatus.processing,
            OrderStatus.processing: OrderStatus.completed,
            OrderStatus.completed: None,
            OrderStatus.cancelled: None
        }
        return status_rules[self.status]
    