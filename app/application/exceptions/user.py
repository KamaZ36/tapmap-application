from dataclasses import dataclass

from app.application.exceptions.base import LogicException


@dataclass(frozen=True)
class UserNotFound(LogicException):
    error_code: str = "USER_NOT_FOUND"

    @property
    def message(self) -> str:
        return "Пользователь не найден"


@dataclass(frozen=True)
class NotSetBaseCityForUser(LogicException):
    error_code = "BASE_CITY_NOT_SET"

    @property
    def message(self) -> str:
        return "У пользователя не установлен город по умолчанию"


@dataclass(frozen=True)
class UserHasBeenBlocked(LogicException):
    error_code = "THE_USER_HAS_BEEN_BLOCKED"

    @property
    def message(self) -> str:
        return "Пользователь заблкоирован"


@dataclass(frozen=True)
class UserBlockNotFound(LogicException):
    error_code = "USER_BLOCK_NOT_FOUND"

    @property
    def message(self) -> str:
        return "Активная блокировка пользователя не найдена."
