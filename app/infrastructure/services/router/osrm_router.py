from app.settings import settings

from app.domain.value_objects.coordinates import Coordinates
from app.infrastructure.exceptions.router import FailedToCalculateRoute

from app.infrastructure.services.http_client.base import BaseHttpClient
from app.infrastructure.services.router.base import BaseRouter


class Router(BaseRouter):
    BASE_URL = settings.router_base_url

    def __init__(self, http_client: BaseHttpClient) -> None:
        self.http_client = http_client

    async def get_distance_route(self, coordinates_list: list[Coordinates]) -> int:
        coordinates = ";".join(
            f"{coordinates.longitude},{coordinates.latitude}"
            for coordinates in coordinates_list
        )
        url = f"{self.BASE_URL}{coordinates}?overview=false"
        response_data = await self.http_client.get(url)
        if not response_data.get("routes"):
            raise FailedToCalculateRoute()
        distance = response_data["routes"][0]["distance"]
        return int(round(distance))
