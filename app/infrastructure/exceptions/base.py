from app.domain.exceptions.base import AppException


class InfrastructureException(AppException):
    
    @property
    def message(self) -> str:
        return "Произошла ошибка инфраструктуры"

class InvalidAccessToken(InfrastructureException):
    error_code = "INVALID_AUTH_TOKEN"
    
    @property
    def message(self) -> str:
        return "Токен авторизации невалиден" 
