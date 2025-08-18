from dataclasses import dataclass
from uuid import UUID

from app.application.commands.order import AddPointToDraftOrderCommand
from app.application.exceptions.city import CityNotFound
from app.application.exceptions.draft_order import DraftOrderNotFound
from app.application.exceptions.user import NotSetBaseCityForUser, UserNotFound

from app.domain.entities.draft_order import DraftOrder

from app.infrastructure.repositories.city.base import BaseCityRepository
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository

from app.services.pricing.pricing_service import PricingService
from app.services.geolocation import GeolocationService


@dataclass
class AddPointToDraftOrderInteraction:
    user_repository: BaseUserRepository
    city_repository: BaseCityRepository
    draft_order_repo: BaseDraftOrderRepository
    geolocation_service: GeolocationService
    pricing_service: PricingService
    
    async def __call__(self, command: AddPointToDraftOrderCommand, user_id: UUID) -> DraftOrder:
        draft_order = await self.draft_order_repo.get_by_customer_id(user_id)
        if not draft_order:
            raise DraftOrderNotFound()
        
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        if user.base_city_id is None:
            raise NotSetBaseCityForUser(user_id=user.id)
    
        city = await self.city_repository.get_by_id(user.base_city_id)
        if not city:
            raise CityNotFound()
    
        point = await self.geolocation_service.resolve_location(location=command.point, city=city)
        points = draft_order.points.copy()
        points.append(point)
        coordinates_list = [point.coordinates for point in points]
        route_info = await self.geolocation_service.get_route_details(coordinates_list)
        price = self.pricing_service.calculate_price(city=city, distance=route_info.travel_distance)
        draft_order.add_point(
            point=point,
            price=price,
            travel_distance=route_info.travel_distance,
            travel_time=route_info.travel_time 
        )
        await self.draft_order_repo.update(draft_order)
        return draft_order
        