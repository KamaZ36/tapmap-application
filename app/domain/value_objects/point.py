from dataclasses import dataclass

from app.domain.value_objects.base import ValueObject
from app.domain.value_objects.coordinates import Coordinates


@dataclass(frozen=True)
class Point(ValueObject): 
    address: str
    coordinates: Coordinates
