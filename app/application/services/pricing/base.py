from typing import Protocol

from app.domain.entities.city import City
from app.domain.value_objects.money import Money


class BasePricingService(Protocol):
    def calculate_price(self, city: City, distance: int) -> Money: ...

    def calculate_commission(self, city: City, price: Money) -> Money: ...
