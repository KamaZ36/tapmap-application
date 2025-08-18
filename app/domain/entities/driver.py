from dataclasses import dataclass

from app.domain.entities.base import Entity
from app.domain.enums.driver_status import DriverStatus
from app.domain.exceptions.driver import DriverAlreadyOnOrder, DriverAlreadyOnShift, DriverIsNotOrder, DriverIsNotShift
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.phone_number import PhoneNumber


@dataclass(kw_only=True)
class Driver(Entity): 
    first_name: str
    last_name: str
    middle_name: str | None = None
    phone_number: PhoneNumber
    
    license_number: str
    
    completed_orders_count: int = 0
    cancelled_orders_count: int = 0
    
    last_location: Coordinates | None = None
    
    status: DriverStatus = DriverStatus.active
    
    on_shift: bool = False
    on_order: bool = False

    def set_shift_status(self, status: bool) -> None:
        self.on_shift = status

    def start_shift(self) -> None: 
        """Выйти на смену

        Raises:
            DriverAlreadyOnShift: Водитель уже на смене
        """
        if self.on_shift: 
            raise DriverAlreadyOnShift()
        self.on_shift = True
    
    def end_shift(self) -> None: 
        """Уйти со смены

        Raises:
            DriverIsNotShift: Водитель не на смене
        """
        if not self.on_shift: 
            raise DriverIsNotShift()
        self.on_shift = False
        
    def assign_to_order(self) -> None: 
        """Назначить водителя на заказ

        Raises:
            DriverIsNotShift: Водитель не на смене
            DriverAlreadyOnOrder: Водитель уже на заказе
        """
        if not self.on_shift: 
            raise DriverIsNotShift()
        if self.on_order: 
            raise DriverAlreadyOnOrder()
        self.on_order = True        

    def complete_order(self) -> None: 
        """Завершить заказ водителя

        Raises:
            DriverIsNotOrder: Водитель не выполняет заказ
        """
        if not self.on_order: 
            raise DriverIsNotOrder()
        self.completed_orders_count += 1
        self.on_order = False
        
    def cancel_order(self) -> None:
        """Отменить заказ водителя

        Raises:
            DriverIsNotOrder: Водитель не выполняет заказ
        """
        if not self.on_order: 
            raise DriverIsNotOrder()
        self.cancelled_orders_count += 1
        self.on_order = False
        
    def update_location(self, coordinates: Coordinates) -> None:
        self.last_location = coordinates
