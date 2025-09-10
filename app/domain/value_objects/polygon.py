from dataclasses import dataclass

from app.domain.exceptions.city import InvalidPolygon
from app.domain.value_objects.base import ValueObject
from app.domain.value_objects.coordinates import Coordinates


@dataclass(frozen=True)
class Polygon(ValueObject):
    points: list[Coordinates]

    def __post_init__(self):
        if len(self.points) < 5:
            raise InvalidPolygon()
