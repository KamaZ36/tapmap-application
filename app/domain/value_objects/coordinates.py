from dataclasses import dataclass

from app.domain.value_objects.base import ValueObject


@dataclass(frozen=True)
class Coordinates(ValueObject):
    latitude: float
    longitude: float

    def __post_init__(self):
        if not (-90 <= self.latitude <= 90):
            raise ValueError(f"Latitude {self.latitude} out of range (-90..90)")
        if not (-180 <= self.longitude <= 180):
            raise ValueError(f"Longitude {self.longitude} out of range (-180..180)")

    def __str__(self) -> str:
        return f"({self.latitude}, {self.longitude})"
