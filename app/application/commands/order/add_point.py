from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand, CommandHandler
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.order_point import OrderPoint

from app.application.commands.converters import convert_order_entities_to_dto
from app.application.dtos.order import OrderDTO
from app.application.exceptions.city import CityNotFound
from app.application.exceptions.geolocation import (
    InaccurateAddress,
    InaccurateGeolocation,
)
from app.application.exceptions.order import OrderNotFound
from app.application.exceptions.user import UserNotFound
from app.application.services.pricing.base import BasePricingService

from app.infrastructure.repositories.city.base import BaseCityRepository
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.services.address_parser.base import BaseAddressParser
from app.infrastructure.services.geocoder.base import BaseGeocoder
from app.infrastructure.services.route_service.base import BaseRouteService


@dataclass
class AddPointToOrderCommand(BaseCommand):
    order_id: UUID
    point: str | tuple[float, float]
    current_user_id: UUID


@dataclass
class AddPointToOrderCommandHandler(CommandHandler[AddPointToOrderCommand, OrderDTO]):
    user_repository: BaseUserRepository
    draft_order_repository: BaseDraftOrderRepository
    geocoder: BaseGeocoder
    route_service: BaseRouteService
    city_repository: BaseCityRepository
    address_parser: BaseAddressParser
    pricing_service: BasePricingService

    async def __call__(self, command: AddPointToOrderCommand) -> OrderDTO:
        order = await self.draft_order_repository.get_by_id(command.order_id)
        if order is None:
            raise OrderNotFound()

        customer = await self.user_repository.get_by_id(order.customer_id)
        if customer is None:
            raise UserNotFound()

        city = await self.city_repository.get_by_id(city_id=order.city_id)
        if city is None:
            raise CityNotFound()

        if isinstance(command.point, tuple):
            location = command.point
            coordinates = Coordinates(latitude=location[0], longitude=location[1])

            geocoded_info = await self.geocoder.get_address(coordinates)
            if geocoded_info is None:
                raise InaccurateGeolocation()

            point = OrderPoint(address=geocoded_info.address, coordinates=coordinates)
        else:
            parsed_start_address = await self.address_parser.parse_address(
                command.point
            )

            if parsed_start_address.city:
                query_address = parsed_start_address.full_address
            else:
                query_address = (
                    f"{city.state}, {city.name}, {parsed_start_address.street}"
                )

            geocoded_info = await self.geocoder.get_coordinates(address=query_address)
            if geocoded_info is None:
                raise InaccurateAddress(address=query_address)

            coordinates = Coordinates(
                latitude=geocoded_info.coordinates[0],
                longitude=geocoded_info.coordinates[1],
            )
            point = OrderPoint(address=geocoded_info.address, coordinates=coordinates)

        travel_distance = await self.route_service.get_distance_route(
            [or_point.coordinates for or_point in order.points] + [point.coordinates]
        )
        travel_time = await self.route_service.get_time_route(travel_distance)

        price = self.pricing_service.calculate_price(
            city=city, distance=travel_distance
        )
        service_commission = self.pricing_service.calculate_commission(
            city=city, price=price
        )

        order.add_point(
            point=point,
            price=price,
            service_commission=service_commission,
            travel_distance=travel_distance,
            travel_time=travel_time,
        )

        await self.draft_order_repository.update(order)

        return convert_order_entities_to_dto(order=order, customer=customer)
