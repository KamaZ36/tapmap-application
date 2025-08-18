from typing import Protocol

from app.domain.entities.city import City
from app.domain.value_objects.money import Money


class BasePricingService(Protocol):
    
     async def calculate_price(self, distance: int, city: City) -> Money: ...
     
     def calculate_commission(self, price: Money, city: City) -> Money: ...
    