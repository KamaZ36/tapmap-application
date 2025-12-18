from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.infrastructure.gateways.message_broker.base import BaseMessageBrokerGateway

from app.core.dependencies.container import container


@asynccontextmanager
async def lifespan(app) -> AsyncGenerator:
    message_broker: BaseMessageBrokerGateway = await container.get(
        BaseMessageBrokerGateway
    )
    await message_broker.start()

    yield

    await app.state.dishka_container.close()
