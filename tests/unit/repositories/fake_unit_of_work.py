from typing import Any
from app.infrastructure.repositories.city.base import BaseCityRepository
from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.order.base import BaseOrderRepository
from app.infrastructure.unit_of_work.base import BaseUnitOfWork
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.repositories.vehicle.base import BaseVehicleRepository

from .fake_order_repository import FakeOrderRepository
from .fake_driver_repository import FakeDriverRepository
from .fake_city_repository import FakeCityRepository
from .fake_user_repository import FakeUserRepository
from .fake_vehicle_repository import FakeVehicleRepository


class FakeUnitOfWork(BaseUnitOfWork):
    
    def __init__(self): 
        self.committed = False
        self.rolled_back = False
        
        self._users = None
        self._drivers = None
        self._orders = None
        self._vehicles = None
        self._cities = None
    
    @property
    def users(self) -> BaseUserRepository:
        if self._users is None:
            self._users = FakeUserRepository()
        return self._users
    
    @property
    def drivers(self) -> BaseDriverRepository:
        if self._drivers is None:
            self._drivers = FakeDriverRepository()
        return self._drivers
    
    @property
    def orders(self) -> BaseOrderRepository:
        if self._orders is None:
            self._orders = FakeOrderRepository()
        return self._orders
    
    @property
    def vehicles(self) -> BaseVehicleRepository:
        if self._vehicles is None:
            self._vehicles = FakeVehicleRepository()
        return self._vehicles
    
    @property
    def cities(self) -> BaseCityRepository:
        if self._cities is None:
            self._cities = FakeCityRepository()
        return self._cities
    
    async def __aenter__(self) -> BaseUnitOfWork:
        return self
    
    async def __aexit__(self, exc_type: Any, exc_value: Any, exc_tb: Any) -> bool:
        if exc_type:
            await self.rollback()
            return False
        else:
            await self.commit()
            return True
    
    async def commit(self) -> None:
        self.committed = True
    
    async def rollback(self) -> None:
        self.rolled_back = True
    