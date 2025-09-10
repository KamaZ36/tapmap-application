from dataclasses import dataclass

from shapely import Polygon

from app.domain.entities.city import City
from app.domain.entities.user import UserRole

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.city.base import BaseCityRepository

from app.application.exceptions.permission import NoAccess
from app.application.commands.city import CreateCityCommand
from app.application.dtos.user import CurrentUser


@dataclass
class CreateCityInteraction:
    city_repository: BaseCityRepository
    transaction_manager: TransactionManager

    async def __call__(
        self, command: CreateCityCommand, current_user: CurrentUser
    ) -> City:
        self._validate_permission(current_user=current_user)
        polygon = Polygon(command.polygon_coords)
        city = City(
            name=command.name,
            state=command.state,
            base_price=command.base_price,
            service_commission_pct=command.service_commission_pct,
            price_per_kilometer=command.price_per_kilometer,
            polygon=polygon,
        )
        await self.city_repository.create(city)
        await self.transaction_manager.commit()
        return city

    def _validate_permission(self, current_user: CurrentUser) -> None:
        if UserRole.admin in current_user.roles:
            return
        raise NoAccess()
