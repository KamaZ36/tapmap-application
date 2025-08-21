from dataclasses import dataclass
from uuid import UUID

from app.application.commands.user import SetBaseUserLocationCommand

from app.application.exceptions.city import CityNotSupported
from app.application.exceptions.user import NotSetBaseCityForUser
from app.domain.value_objects.coordinates import Coordinates

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.city.base import BaseCityRepository
from app.infrastructure.repositories.user.base import BaseUserRepository


@dataclass
class SetBaseLocationUserInteraction:
    user_repository: BaseUserRepository
    city_repository: BaseCityRepository
    transaction_manager: TransactionManager
    
    async def __call__(self, command: SetBaseUserLocationCommand, user_id: UUID) -> None:
        coordinates = Coordinates(
            latitude=command.coordinates[0],
            longitude=command.coordinates[1]
        )
        city = await self.city_repository.get_by_into_point(coordinates)
        if city is None:
            raise CityNotSupported() 
        user = await self.user_repository.get_by_id(user_id)
        user.set_base_city(city.id)
        await self.user_repository.update(user)
        await self.transaction_manager.commit()
    