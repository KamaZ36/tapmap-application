from functools import lru_cache
from dishka import AsyncContainer, make_async_container

from app.core.dependencies.auth import AuthServices
from app.core.dependencies.base import BaseAppProvider
from app.core.dependencies.command_handlers import CommandHandlersProvider
from app.core.dependencies.query_handlers import QueryHandlersProvider
from app.core.dependencies.readers import ReadersProvider
from app.core.dependencies.repositories import RepositoriesProvider
from app.core.dependencies.services import Services
from app.core.dependencies.tg_bots import TgBotProvider


def make_base_providers():
    return (
        BaseAppProvider(),
        RepositoriesProvider(),
        ReadersProvider(),
        CommandHandlersProvider(),
        QueryHandlersProvider(),
        AuthServices(),
        Services(),
        TgBotProvider(),
    )


container = make_async_container(*make_base_providers())
