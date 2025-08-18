from dataclasses import dataclass, field
from uuid import UUID

from app.domain.entities.base import Entity
from app.domain.exceptions.draft_order import ConsecutiveDuplicatePointError, InvalidRoutePointIndexError
from app.domain.value_objects.money import Money
from app.domain.value_objects.order_comment import OrderComment
from app.domain.value_objects.point import Point


@dataclass(kw_only=True)
class DraftOrder(Entity):
    customer_id: UUID
    city_id: UUID
    points: list[Point] = field(default_factory=list)
    price: Money
    travel_distance: int
    travel_time: int 
    comment: OrderComment | None = None
    

    def add_point(self, point: Point, price: Money, travel_time: int, travel_distance: int) -> None: 
        """Добавить точку маршрута в маршрут заказа

        Args:
            point (Point): Точка для добавления
            price (Money): Пересчитанная цена
            service_commission (Money): Пересчитанная комиссия сервиса

        Raises:
            ConsecutiveDuplicatePointError: Точка совпадает с предыдущей
        """
        if self.points[-1] == point: 
            raise ConsecutiveDuplicatePointError(new_point=point, prev_point=self.points[-1])
        self.points.append(point)
        self._update_price(price=price)
        self._update_route_info(travel_time=travel_time, travel_distance=travel_distance)

    def delete_point(self, index: int, price: Money) -> None:
        """Удалить точку маршрута из маршрута заказа

        Args:
            index (int): Индекс точки в списке маршрута
            price (Money): Пересчитанная цена
            service_commission (Money): Пересчитанная комиссия сервиса

        Raises:
            InvalidRoutePointIndexError: Индекс меньше нуля или больше списка маршрута
        """
        if index < 0 or index >= len(self.points): 
            raise InvalidRoutePointIndexError(index=index, route_len=len(self.points))
        del self.points[index]
        self._update_price(price=price)

    def add_comment(self, comment: OrderComment) -> None:
        self.comment = comment

    def _update_price(self, price: Money) -> None:
        self.price = price
        
    def _update_route_info(self, travel_time: int, travel_distance: int) -> None:
        self.travel_distance = travel_distance
        self.travel_time = travel_time
