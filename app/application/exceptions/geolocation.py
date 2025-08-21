from dataclasses import dataclass

from app.application.exceptions.base import LogicException


@dataclass
class GeocodingServiceUnavailable(LogicException):
    error_code: str = "GEOCODER_UNAVAILABLE"

    @property
    def message(self) -> str:
        return "Сервис геокодинга недоступен. Попробуйте позже."
