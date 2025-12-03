from dataclasses import dataclass

from app.application.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class GeocodingServiceUnavailable(LogicException):
    error_code: str = "GEOCODER_UNAVAILABLE"

    @property
    def message(self) -> str:
        return "Сервис геокодинга недоступен. Попробуйте позже."


@dataclass(frozen=True, eq=False, kw_only=True)
class InaccurateAddress(LogicException):
    error_code: str = "INACCURATE_ADDRESS"
    address: str

    @property
    def message(self) -> str:
        return f"Неточно указан адрес: {self.address}"


@dataclass(frozen=True, eq=False, kw_only=True)
class InaccurateGeolocation(LogicException):
    error_code: str = "INACCURATE_ADDRESS"

    @property
    def message(self) -> str:
        return "Неточно указана геолокация"
