from dishka import Provider, provide, Scope

from app.infrastructure.gateways.geocoder.base import BaseGeocoderGateway
from app.infrastructure.gateways.geocoder.open_cage_geocoder import (
    OpenCageGeocoderGateway,
)
from app.infrastructure.gateways.routes.base import BaseRouteInfoGateway
from app.infrastructure.gateways.routes.osrm_router import OSRMRouteInfoGateway
from app.infrastructure.services.http_client.base import BaseHttpClient


class GatewaysProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_route_gateway(self, http_client: BaseHttpClient) -> BaseRouteInfoGateway:
        return OSRMRouteInfoGateway(http_client)

    @provide(scope=Scope.REQUEST)
    def get_geocoder_gateway(self, http_client: BaseHttpClient) -> BaseGeocoderGateway:
        return OpenCageGeocoderGateway(http_client)
