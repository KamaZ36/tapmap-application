from dataclasses import dataclass

from app.domain.exceptions.base import AppException


@dataclass
class InvalidPolygon(AppException):
    @property
    def message(self) -> str:
        return "Некорректный полигон города"
