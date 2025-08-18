from dataclasses import dataclass

from app.application.exceptions.base import LogicException


@dataclass
class NoAccess(LogicException):

    @property
    def message(self) -> str:
        return "Нет доступа."
