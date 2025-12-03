from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand, CommandHandler
from app.application.commands.converters import convert_order_entities_to_dto
from app.domain.value_objects.order_point import OrderPoint
from app.domain.entities.order import Order
from app.domain.value_objects.coordinates import Coordinates

from app.application.services.user_service import UserService
from app.application.exceptions.geolocation import (
    InaccurateAddress,
    InaccurateGeolocation,
)
from app.application.exceptions.city import CityNotSupported
from app.application.exceptions.user import (
    NotSetBaseCityForUser,
    UserHasBeenBlocked,
    UserNotFound,
)
from app.application.dtos.order import OrderDTO

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.city.base import BaseCityRepository
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.services.address_parser.base import BaseAddressParser
from app.infrastructure.services.geocoder.base import BaseGeocoder


@dataclass
class CreateOrderCommand(BaseCommand):
    current_user_id: UUID
    user_id: UUID
    start_point: str | tuple[float, float]


@dataclass(eq=False)
class CreateOrderCommandHandler(CommandHandler[CreateOrderCommand, OrderDTO]):
    draft_order_repository: BaseDraftOrderRepository
    user_repository: BaseUserRepository
    city_repository: BaseCityRepository
    user_service: UserService
    geocoder: BaseGeocoder
    address_parser: BaseAddressParser
    transaction_manager: TransactionManager

    async def __call__(self, command: CreateOrderCommand) -> OrderDTO:
        customer = await self.user_repository.get_by_id(command.user_id)
        if customer is None:
            raise UserNotFound()

        if await self.user_service.check_user_blocking(customer.id):
            raise UserHasBeenBlocked()

        city = None

        if isinstance(command.start_point, tuple):
            coordinates = Coordinates(
                latitude=command.start_point[0], longitude=command.start_point[1]
            )
            city = await self.city_repository.get_by_into_point(coordinates)
            if city is None:
                raise CityNotSupported()

            geocoded_info = await self.geocoder.get_address(coordinates)
            if geocoded_info is None:
                raise InaccurateGeolocation()

            point = OrderPoint(address=geocoded_info.address, coordinates=coordinates)

        else:
            raw_address = command.start_point
            parsed_address = await self.address_parser.parse_address(raw_address)

            if parsed_address.city:
                query_address = parsed_address.full_address
            else:
                if customer.base_city_id is None:
                    raise NotSetBaseCityForUser()
                city = await self.city_repository.get_by_id(customer.base_city_id)
                if city is None:
                    raise CityNotSupported()
                query_address = f"{city.state}, {city.name}, {parsed_address.street}"

            geocoded_info = await self.geocoder.get_coordinates(address=query_address)
            if geocoded_info is None:
                raise InaccurateAddress(address=raw_address)

            coordinates = Coordinates(
                latitude=geocoded_info.coordinates[0],
                longitude=geocoded_info.coordinates[1],
            )

            point = OrderPoint(address=geocoded_info.address, coordinates=coordinates)

            if parsed_address.city:
                city = await self.city_repository.get_by_into_point(point.coordinates)

        if city is None:
            raise CityNotSupported()

        order = Order(
            customer_id=customer.id,
            city_id=city.id,
            points=[point],
            price=None,
            service_commission=None,
            travel_distance=None,
            travel_time=None,
        )

        if customer.base_city_id != city.id:
            customer.set_base_city(city.id)
            await self.user_repository.update(customer)

        await self.draft_order_repository.create(order)
        await self.transaction_manager.commit()

        return convert_order_entities_to_dto(order=order, customer=customer)
