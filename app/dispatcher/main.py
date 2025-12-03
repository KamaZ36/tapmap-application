from faststream import FastStream
from faststream.redis import RedisBroker

from app.core.config import settings

from app.dispatcher.handlers import router


def add_routers(broker: RedisBroker) -> None:
    broker.include_router(router=router)


def get_app() -> FastStream:
    broker = RedisBroker(settings.redis_url)

    add_routers(broker)

    return FastStream(broker=broker)
