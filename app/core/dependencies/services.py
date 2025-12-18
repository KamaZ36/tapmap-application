from dishka import Provider, provide, Scope

from app.application.services.geocoding_service import GeocodingService
from app.application.services.pricing.base import BasePricingService
from app.application.services.pricing.pricing_service import PricingService
from app.application.services.route_service import RouteService
from app.application.services.user_service import UserService

from app.infrastructure.services.address_parser.base import BaseAddressParser
from app.infrastructure.services.address_parser.regex_parser import RegexAddressParser


class Services(Provider):
    scope = Scope.REQUEST

    user_servie = provide(UserService)

    geocoding_serivce = provide(GeocodingService)
    route_service = provide(RouteService)

    @provide(scope=Scope.REQUEST)
    def get_pricing_service(self) -> BasePricingService:
        return PricingService()

    @provide(scope=Scope.REQUEST)
    def get_address_parser(self) -> BaseAddressParser:
        return RegexAddressParser()
