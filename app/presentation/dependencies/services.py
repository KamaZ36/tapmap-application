from dishka import Provider, provide, Scope

from app.application.services.pricing.pricing_service import PricingService
from app.application.services.geolocation import GeolocationService

from app.infrastructure.services.geocoder.base import BaseGeocoder
from app.infrastructure.services.geocoder.open_cage_geocoder import Geocoder
from app.infrastructure.services.http_client.base import BaseHttpClient
from app.infrastructure.services.router.base import BaseRouter
from app.infrastructure.services.router.osrm_router import Router


class Services(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.REQUEST)
    def get_pricing_service(self) -> PricingService:
        return PricingService()

    @provide(scope=Scope.REQUEST)
    def get_geocoder(self, http_client: BaseHttpClient) -> BaseGeocoder:
        return Geocoder(http_client)

    @provide(scope=Scope.REQUEST)
    def get_router(self, http_client: BaseHttpClient) -> BaseRouter:
        return Router(http_client)

    @provide(scope=Scope.REQUEST)
    def get_geolocation_service(
        self, router: BaseRouter, geocoder: BaseGeocoder
    ) -> GeolocationService:
        return GeolocationService(geocoder=geocoder, router=router)
