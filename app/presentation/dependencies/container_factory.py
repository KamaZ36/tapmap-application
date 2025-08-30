from dishka import make_async_container

from app.presentation.dependencies.auth import AuthServices
from app.presentation.dependencies.base import BaseAppProvider
from app.presentation.dependencies.repositories import RepositoriesProvider
from app.presentation.dependencies.interactors import Interactors
from app.presentation.dependencies.services import Services


def make_base_providers():
    return (
        BaseAppProvider(),
        RepositoriesProvider(),
        Interactors(),
        AuthServices(),
        Services(),
    )


def make_base_container():
    return make_async_container(*make_base_providers())


