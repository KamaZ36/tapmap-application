from dishka import Provider, provide, Scope

from app.application.services.pricing.base import BasePricingService
from app.application.services.pricing.pricing_service import PricingService
from app.application.services.user_service import UserService

from app.infrastructure.services.address_parser.base import BaseAddressParser
from app.infrastructure.services.address_parser.regex_parser import RegexAddressParser
from app.infrastructure.services.geocoder.base import BaseGeocoder
from app.infrastructure.services.geocoder.open_cage_geocoder import Geocoder
from app.infrastructure.services.http_client.base import BaseHttpClient
from app.infrastructure.services.route_service.base import BaseRouteService
from app.infrastructure.services.route_service.osrm_router import OSRMRouteService


class Services(Provider):
    scope = Scope.REQUEST

    user_servie = provide(UserService)

    @provide(scope=Scope.REQUEST)
    def get_pricing_service(self) -> BasePricingService:
        return PricingService()

    @provide(scope=Scope.REQUEST)
    def get_geocoder(self, http_client: BaseHttpClient) -> BaseGeocoder:
        return Geocoder(http_client)

    @provide(scope=Scope.REQUEST)
    def get_router(self, http_client: BaseHttpClient) -> BaseRouteService:
        return OSRMRouteService(http_client)

    @provide(scope=Scope.REQUEST)
    def get_address_parser(self) -> BaseAddressParser:
        return RegexAddressParser()
