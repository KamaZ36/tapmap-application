from dataclasses import dataclass

from app.domain.exceptions.base import AppException 


@dataclass
class LogicException(AppException):
    
    @property
    def message(self) -> str:
        return "При обработке запроса произошла ошибка"
