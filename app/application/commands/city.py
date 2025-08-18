from dataclasses import dataclass
from decimal import Decimal
from app.application.commands.base import BaseCommand


@dataclass(frozen=True)
class CreateCityCommand(BaseCommand):
    name: str
    state: str
    base_price: Decimal
    price_per_kilometer: Decimal
    service_commission_pct: Decimal
    polygon_coords: list[tuple[float, float]]
