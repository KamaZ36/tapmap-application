from app.infrastructure.exceptions.base import InfrastructureException


class InvalidAccessToken(InfrastructureException):
    error_code = "INVALID_AUTH_TOKEN"

    @property
    def message(self) -> str:
        return "Токен авторизации невалиден"
