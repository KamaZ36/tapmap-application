from dishka import Provider, provide, Scope

from app.application.services.pricing.pricing_service import PricingService

from app.services.geocoder.base import BaseGeocoder
from app.services.geocoder.open_cage_geocoder import Geocoder
from app.services.geolocation import GeolocationService
from app.services.router.base import BaseRouter
from app.services.router.osrm_router import Router

from app.services.http_client import http_client


class Services(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.REQUEST)
    def get_pricing_service(self) -> PricingService:
        return PricingService()
    
    @provide(scope=Scope.REQUEST)
    def get_geocoder(self) -> BaseGeocoder:
        return Geocoder(http_client)
    
    @provide(scope=Scope.REQUEST)
    def get_router(self) -> BaseRouter:
        return Router(http_client)
    
    @provide(scope=Scope.REQUEST)
    def get_geolocation_service(self, router: BaseRouter, geocoder: BaseGeocoder) -> GeolocationService:
        return GeolocationService(geocoder=geocoder, router=router)
    