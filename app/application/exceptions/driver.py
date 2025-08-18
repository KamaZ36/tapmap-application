from app.application.exceptions.base import LogicException


class DriverNotFound(LogicException):
    
    @property
    def message(self) -> str:
        return "Водитель не найден"    
