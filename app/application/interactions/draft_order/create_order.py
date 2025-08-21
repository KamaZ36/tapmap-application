import asyncio

from dataclasses import dataclass
from uuid import UUID


from app.application.commands.order import CreateDraftOrderCommand

from app.domain.entities.draft_order import DraftOrder
from app.domain.entities.city import City
from app.domain.value_objects.point import Point

from app.infrastructure.repositories.city.base import BaseCityRepository
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository

from app.application.exceptions.user import NotSetBaseCityForUser, UserNotFound

from app.application.services.pricing.pricing_service import PricingService
from app.services.geolocation import GeolocationService


@dataclass
class CreateDraftOrderInteraction:
    user_repository: BaseUserRepository
    city_repository: BaseCityRepository
    draft_order_repository: BaseDraftOrderRepository
    geolocation_service: GeolocationService
    pricing_service: PricingService
        
    async def __call__(self, command: CreateDraftOrderCommand, user_id: UUID) -> DraftOrder | None:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFound()
        if not user.base_city_id:
            raise NotSetBaseCityForUser()
        city = await self.city_repository.get_by_id(user.base_city_id)
        
        points = await self._create_points(command, city)            
        route_info = await self.geolocation_service.get_route_details([point.coordinates for point in points])
        price = self.pricing_service.calculate_price(city=city, distance=route_info.travel_distance)
        
        draft_order = DraftOrder(
            customer_id=user.id,
            city_id=user.base_city_id,
            points=points,
            price=price,
            travel_distance=route_info.travel_distance,
            travel_time=route_info.travel_time, 
        )
        
        await self.draft_order_repository.create(draft_order)
        
        return draft_order
            
    
    async def _create_points(self, command: CreateDraftOrderCommand, city: City) -> list[Point]:
        start_point, end_point = await asyncio.gather(
            self.geolocation_service.resolve_location(location=command.start_point, city=city),
            self.geolocation_service.resolve_location(location=command.end_point, city=city)
        )
        return [start_point, end_point]
    