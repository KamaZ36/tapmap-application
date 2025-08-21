from dataclasses import dataclass

from app.domain.exceptions.base import AppException 


@dataclass
class LogicException(AppException):
    error_code: str = "LOGIC_ERROR"
    
    @property
    def message(self) -> str:
        return "При обработке запроса произошла ошибка"
