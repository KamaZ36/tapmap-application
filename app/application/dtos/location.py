from dataclasses import dataclass


@dataclass
class CoordinatesDTO:
    latitude: float
    longitude: float

@dataclass
class PointDTO:
    address: str | None = None
    coordinates: tuple[float, float] | None = None

@dataclass
class RouteInfoDTO:
    travel_distance: int
    travel_time: int
