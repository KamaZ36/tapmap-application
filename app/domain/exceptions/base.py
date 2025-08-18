from dataclasses import dataclass


@dataclass
class AppException(Exception):
    
    @property
    def message(self) -> str:
        return "Произошла ошибка приложения"
    