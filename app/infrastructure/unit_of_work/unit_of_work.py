from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.repositories.city.sqlalchemy_repository import SQLAlchemyCityRepository
from app.infrastructure.repositories.driver.sqlalchemy_repository import SQLAlchemyDriverRepository
from app.infrastructure.repositories.order.sqlalchemy_repository import SQLAlchemyOrderRepository
from app.infrastructure.unit_of_work.base import BaseUnitOfWork
from app.infrastructure.repositories.user.sqlalchemy_repository import SQLAlchemyUserRepository
from app.infrastructure.repositories.vehicle.sqlalchemy_repository import SQLAlhcemyVehicleRepository


class UnitOfWork(BaseUnitOfWork): 
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self._users = None
        self._drivers = None
        self._cities = None
        self._vehicles = None
        self._orders = None
        
    
    @property
    def users(self) -> SQLAlchemyUserRepository:
        if self._users is None:
            self._users = SQLAlchemyUserRepository(session=self.session)
        return self._users
    
    @property
    def drivers(self) -> SQLAlchemyDriverRepository:
        if self._drivers is None:
            self._drivers = SQLAlchemyDriverRepository(session=self.session)
        return self._drivers
    
    @property
    def vehicles(self) -> SQLAlhcemyVehicleRepository:
        if self._vehicles is None:
            self._vehicles = SQLAlhcemyVehicleRepository(session=self.session)
        return self._vehicles
    
    @property 
    def cities(self) -> SQLAlchemyCityRepository:
        if self._cities is None:
            self._cities = SQLAlchemyCityRepository(session=self.session)
        return self._cities
    
    @property
    def orders(self) -> SQLAlchemyOrderRepository:
        if self._orders is None:
            self._orders = SQLAlchemyOrderRepository(session=self.session)
        return self._orders
    
    async def __aenter__(self) -> BaseUnitOfWork:
        return self
    
    async def __aexit__(self, exc_type, exc_value, exc_tb) -> bool:
        if exc_type:
            await self.rollback()
            return False
        else:
            await self.commit()
            return True
            
    async def commit(self) -> None:
        await self.session.commit()
        
    async def rollback(self) -> None:
        await self.session.rollback()
