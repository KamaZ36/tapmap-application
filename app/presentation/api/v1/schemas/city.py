from decimal import Decimal
from pydantic import BaseModel


class CreateCitySchema(BaseModel): 
    name: str
    state: str
    base_price: Decimal
    price_per_kilometer: Decimal
    service_commission_pct: Decimal
    polygon_coords: list[tuple[float, float]]
