from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions.base import LogicException


@dataclass
class UserNotFound(LogicException):
    error_code: str = "USER_NOT_FOUND"

    @property
    def message(self) -> str:
        return "Пользователь не найден"


@dataclass
class NotSetBaseCityForUser(LogicException):
    error_code = "BASE_CITY_NOT_SET"

    @property
    def message(self) -> str:
        return f"У пользователя не установлен город по умолчанию"
