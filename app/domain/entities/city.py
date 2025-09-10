from dataclasses import dataclass
from decimal import Decimal

from shapely.geometry import Point as SH_Point
from shapely import Polygon, LineString

from app.domain.entities.base import Entity
from app.domain.exceptions.city import InvalidPolygon
from app.domain.value_objects.order_point import OrderPoint


@dataclass
class City(Entity):
    name: str
    state: str

    base_price: Decimal
    price_per_kilometer: Decimal
    service_commission_pct: Decimal

    polygon: Polygon

    def is_point_inside(self, point: OrderPoint) -> bool:
        latitude, longitude = point.coordinates.latitude, point.coordinates.longitude
        return self.polygon.contains(SH_Point((latitude, longitude)))

    def is_route_inside(self, points: list[OrderPoint]) -> bool:
        route_line = LineString(
            [
                (point.coordinates.latitude, point.coordinates.longitude)
                for point in points
            ]
        )
        return self.polygon.contains(route_line)

    def get_center(self) -> tuple[float, float]:
        centroid = self.polygon.centroid
        return (centroid.x, centroid.y)

    def intersects_with(self, other_city: "City") -> bool:
        return self.polygon.intersects(other_city.polygon)

    def __str__(self) -> str:
        return f"{self.name}, {self.state}"
