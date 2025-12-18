from dataclasses import dataclass


@dataclass(kw_only=True)
class ParsedAddressDTO:
    city: str | None = None
    street: str
    full_address: str


@dataclass(kw_only=True, frozen=True)
class RouteInfoDTO:
    distance: int
    travel_time: int


@dataclass(frozen=True, eq=False)
class GeocodedInfoDTO:
    address: str
    coordinates: tuple[float, float]
