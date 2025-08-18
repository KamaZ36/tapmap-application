from typing import Protocol

from app.infrastructure.repositories.city.base import BaseCityRepository
from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.order.base import BaseOrderRepository
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.repositories.vehicle.base import BaseVehicleRepository


class BaseUnitOfWork(Protocol): 
    
    async def __aenter__(self) -> 'BaseUnitOfWork': ...
    
    async def __aexit__(self, exc_type, exc_value, exc_tb) -> bool: ...
     
    async def commit(self) -> None: ...
    
    async def rollback(self) -> None: ...
    
    @property
    def users(self) -> BaseUserRepository: ...
    
    @property
    def drivers(self) -> BaseDriverRepository: ...
    
    @property
    def vehicles(self) -> BaseVehicleRepository: ...
    
    @property
    def cities(self) -> BaseCityRepository: ...
    
    @property
    def orders(self) -> BaseOrderRepository: ...
    