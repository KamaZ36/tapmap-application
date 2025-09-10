import pytest
from app.domain.value_objects.order_point import OrderPoint
from app.domain.value_objects.coordinates import Coordinates


def test_create_point_success() -> None:
    coords = Coordinates(latitude=55.7558, longitude=37.6173)
    point = OrderPoint(address="Москва, Красная площадь", coordinates=coords)

    assert point.address == "Москва, Красная площадь"
    assert point.coordinates == coords
    assert point.coordinates.latitude == 55.7558
    assert point.coordinates.longitude == 37.6173


def test_point_immutable() -> None:
    coords = Coordinates(latitude=55.7558, longitude=37.6173)
    point = OrderPoint(address="Москва", coordinates=coords)
    with pytest.raises(Exception):
        point.address = "СПб"  # Пытаемся изменить
