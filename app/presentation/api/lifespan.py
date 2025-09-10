from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.infrastructure.services.message_broker.base import BaseMessageBroker

from app.presentation.dependencies.container import container


@asynccontextmanager
async def lifespan(app) -> AsyncGenerator:
    message_broker: BaseMessageBroker = await container.get(BaseMessageBroker)
    await message_broker.start()

    yield

    await app.state.dishka_container.close()
