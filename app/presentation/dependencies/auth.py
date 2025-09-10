from dishka import Provider, Scope, provide

from app.infrastructure.services.auth.authentication import AuthenticationService


class AuthServices(Provider):
    authentication_service = provide(AuthenticationService, scope=Scope.REQUEST)
