from app.application.dtos.location import RouteInfoDTO
from app.domain.value_objects.coordinates import Coordinates
from app.infrastructure.gateways.routes.base import BaseRouteInfoGateway


class RouteService:
    def __init__(self, router_gateway: BaseRouteInfoGateway) -> None:
        self.router_gateway = router_gateway

    async def get_route_info(self, coordinates_list: list[Coordinates]) -> RouteInfoDTO:
        distance = await self.router_gateway.get_distance_route(coordinates_list)
        travel_time = await self.get_route_travel_time(distance)
        return RouteInfoDTO(distance=distance, travel_time=travel_time)

    async def get_route_distance(self, coordinates_list: list[Coordinates]) -> int:
        distance = await self.router_gateway.get_distance_route(coordinates_list)
        return distance

    async def get_route_travel_time(self, distance: int) -> int:
        travel_time = int(round((float(distance) / 1000) / 50 * 60 + 2))
        return travel_time
