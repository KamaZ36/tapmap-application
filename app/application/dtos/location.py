from dataclasses import dataclass


@dataclass
class CoordinatesDTO:
    latitude: float
    longitude: float

@dataclass
class PointDTO:
    address: str | None = None
    coordinates: tuple[float, float] | None = None
