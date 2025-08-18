from dataclasses import dataclass

from app.domain.exceptions.base import AppException
from app.domain.value_objects.point import Point


@dataclass
class ConsecutiveDuplicatePointError(AppException):
    new_point: Point
    prev_point: Point
    
    @property
    def message(self) -> str:
        new_point_coordinates = self.new_point.coordinates
        prev_point_coordinates = self.prev_point.coordinates
        
        return f"Новая точка ({new_point_coordinates}) совпадает с предыдущей ({prev_point_coordinates})"

@dataclass
class InvalidRoutePointIndexError(AppException):
    index: int
    route_len: int
    
    @property
    def message(self) -> str:
        return f"Индекс ({self.index}) меньше нуля или больше списка маршрута {self.route_len}."
