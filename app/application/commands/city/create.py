from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID
from shapely import Polygon

from app.domain.entities.city import City
from app.domain.entities.user import User, UserRole

from app.application.dtos.city import CityDTO
from app.application.commands.converters import convert_city_entity_to_dto
from app.application.commands.base import BaseCommand, CommandHandler
from app.application.exceptions.user import UserNotFound
from app.application.exceptions.permission import NoAccess

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.city.base import BaseCityRepository
from app.infrastructure.repositories.user.base import BaseUserRepository


@dataclass(frozen=True)
class CreateCityCommand(BaseCommand):
    current_user_id: UUID
    name: str
    state: str
    base_price: Decimal
    price_per_kilometer: Decimal
    service_commission: Decimal
    polygon_coords: list[tuple[float, float]]


@dataclass
class CreateCityInteraction(CommandHandler[CreateCityCommand, CityDTO]):
    user_repository: BaseUserRepository
    city_repository: BaseCityRepository
    transaction_manager: TransactionManager

    async def __call__(self, command: CreateCityCommand) -> CityDTO:
        user = await self.user_repository.get_by_id(command.current_user_id)
        if user is None:
            raise UserNotFound()

        self._validate_permission(current_user=user)

        polygon = Polygon(command.polygon_coords)
        city = City(
            name=command.name,
            state=command.state,
            base_price=command.base_price,
            service_commission_pct=command.service_commission,
            price_per_kilometer=command.price_per_kilometer,
            polygon=polygon,
        )
        await self.city_repository.create(city)
        await self.transaction_manager.commit()
        return convert_city_entity_to_dto(city)

    def _validate_permission(self, current_user: User) -> None:
        if UserRole.admin in current_user.roles:
            return
        raise NoAccess()
