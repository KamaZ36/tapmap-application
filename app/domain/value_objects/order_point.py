from dataclasses import dataclass

from app.domain.value_objects.base import ValueObject
from app.domain.value_objects.coordinates import Coordinates


@dataclass(frozen=True)
class OrderPoint(ValueObject):
    address: str
    coordinates: Coordinates
