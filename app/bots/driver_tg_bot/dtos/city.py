from dataclasses import dataclass


@dataclass
class CreateCityDTO:
    name: str | None = None
    state: str | None = None
    base_price: float | None = None
    price_per_kilometer: float | None = None
    service_commission_pct: float | None = None
    polygon_coords: list[tuple[float, float]] | None = None
