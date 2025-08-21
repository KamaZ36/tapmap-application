from dataclasses import dataclass

from app.application.exceptions.base import LogicException


@dataclass
class NoAccess(LogicException):
    error_code: str = "NO_ACCESS"

    @property
    def message(self) -> str:
        return "Нет доступа."
