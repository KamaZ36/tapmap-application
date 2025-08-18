from app.domain.exceptions.base import AppException


class InfrastructureException(AppException):
    
    @property
    def message(self) -> str:
        return "Произошла ошибка инфраструктуры"
    