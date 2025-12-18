from dishka import Provider, provide, Scope

from app.application.services.address_parser import AddressParser
from app.application.services.geocoding_service import GeocodingService
from app.application.services.message_broker import MessageBrokerService
from app.application.services.pricing_service import PricingService
from app.application.services.route_service import RouteService
from app.application.services.user_service import UserService


class Services(Provider):
    scope = Scope.REQUEST

    user_servie = provide(UserService)

    geocoding_serivce = provide(GeocodingService)
    route_service = provide(RouteService)

    message_broker = provide(MessageBrokerService)

    address_parser = provide(AddressParser)

    pricing_service = provide(PricingService)
