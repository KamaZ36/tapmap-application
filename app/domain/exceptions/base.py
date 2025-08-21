from dataclasses import dataclass


@dataclass(kw_only=True)
class AppException(Exception):
    error_code: str = "APP_ERROR"
    
    @property
    def message(self) -> str:
        return "Произошла ошибка приложения"
    