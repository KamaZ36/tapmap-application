from decimal import Decimal
from app.domain.entities.city import City
from app.domain.value_objects.money import Money


class PricingService: 
    
    def calculate_price(self, city: City, distance: int) -> Money:
        amount = city.base_price + (city.price_per_kilometer * Decimal(distance / 1000))
        return Money(amount)

    def calculate_commission(self, city: City, price: Money) -> Money:
        commission = price * city.service_commission_pct
        return commission
    