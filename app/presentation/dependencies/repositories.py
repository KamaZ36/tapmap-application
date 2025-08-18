from dishka import Provider, Scope, provide

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.repositories.city.base import BaseCityRepository
from app.infrastructure.repositories.city.sqlalchemy_repository import SQLAlchemyCityRepository
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository
from app.infrastructure.repositories.draft_order.redis_repository import RedisDraftOrderRepository
from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.driver.sqlalchemy_repository import SQLAlchemyDriverRepository
from app.infrastructure.repositories.order.base import BaseOrderRepository
from app.infrastructure.repositories.order.sqlalchemy_repository import SQLAlchemyOrderRepository
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.repositories.user.sqlalchemy_repository import SQLAlchemyUserRepository
from app.infrastructure.repositories.vehicle.base import BaseVehicleRepository
from app.infrastructure.repositories.vehicle.sqlalchemy_repository import SQLAlhcemyVehicleRepository


class RepositoriesProvider(Provider):
    
    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> BaseUserRepository:
        return SQLAlchemyUserRepository(session=session)
    
    @provide(scope=Scope.REQUEST)
    def get_driver_repository(self, session: AsyncSession) -> BaseDriverRepository:
        return SQLAlchemyDriverRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_order_repository(self, session: AsyncSession) -> BaseOrderRepository:
        return SQLAlchemyOrderRepository(session=session)
    
    @provide(scope=Scope.REQUEST)
    def get_vehicle_repository(self, session: AsyncSession) -> BaseVehicleRepository:
        return SQLAlhcemyVehicleRepository(session=session)
    
    @provide(scope=Scope.REQUEST)
    def get_city_repository(self, session: AsyncSession) -> BaseCityRepository:
        return SQLAlchemyCityRepository(session=session)
    
    @provide(scope=Scope.REQUEST)
    def get_draft_order_repository(self, redis: Redis) -> BaseDraftOrderRepository:
        return RedisDraftOrderRepository(redis=redis)
    