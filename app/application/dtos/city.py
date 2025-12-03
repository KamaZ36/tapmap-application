from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from shapely import Polygon


@dataclass(frozen=True, eq=False, kw_only=True)
class CityDTO:
    id: UUID

    name: str
    state: str

    base_price: Decimal
    price_per_kilometer: Decimal
    service_commission_pct: Decimal

    polygon: Polygon
