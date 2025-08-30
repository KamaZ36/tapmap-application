from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.presentation.dependencies.container import container
from app.services.message_broker.base import BaseMessageBroker


@asynccontextmanager
async def lifespan(app) -> AsyncGenerator:
    # Start message broker
    message_broker: BaseMessageBroker = await container.get(BaseMessageBroker)
    await message_broker.start()
    
    yield
    
    # Cleanup
    await app.state.dishka_container.close()
