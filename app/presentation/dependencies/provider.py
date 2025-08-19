from dishka import Provider, Scope, provide
from aiokafka import AIOKafkaProducer

from redis.asyncio import Redis

from app.infrastructure.redis.connection import get_redis_client

from app.config import settings

from app.services.message_broker.redis_broker import RedisMessageBroker
from app.services.pricing.pricing_service import PricingService
from app.services.http_client import http_client
from app.services.geocoder.base import BaseGeocoder
from app.services.geocoder.open_cage_geocoder import Geocoder
from app.services.geolocation import GeolocationService
from app.services.message_broker.base import BaseMessageBroker
from app.services.message_broker.kafka_broker import KafkaMessageBroker
from app.services.router.base import BaseRouter
from app.services.router.osrm_router import Router


class AppProvider(Provider):

    @provide(scope=Scope.APP)
    def get_redis_client(self) -> Redis:
        return get_redis_client()
    
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

    @provide(scope=Scope.APP)
    def get_kafka_message_broker(self, redis: Redis) -> BaseMessageBroker:
        return RedisMessageBroker(redis=redis)
        # return KafkaMessageBroker(producer=AIOKafkaProducer(
        #     bootstrap_servers=settings.kafka_url
        # ))
