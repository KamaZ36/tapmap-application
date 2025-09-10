import pytest
from decimal import Decimal
from shapely import Polygon

from app.domain.entities.city import City, InvalidPolygon
from app.domain.value_objects.order_point import OrderPoint, Coordinates


@pytest.fixture
def valid_polygon():
    """Возвращает валидный полигон (прямоугольник вокруг Москвы)"""
    return Polygon(
        [(55.5, 37.3), (55.5, 37.8), (55.9, 37.8), (55.9, 37.3), (55.5, 37.3)]
    )


@pytest.fixture
def invalid_polygon():
    """Возвращает невалидный полигон (самопересекающийся)"""
    return Polygon(
        [(55.5, 37.3), (55.9, 37.8), (55.5, 37.8), (55.9, 37.3), (55.5, 37.3)]
    )


@pytest.fixture
def moscow_city(valid_polygon):
    return City(
        name="Москва",
        state="Московская область",
        base_price=Decimal("100.0"),
        price_per_kilometer=Decimal("10.0"),
        service_commission_pct=Decimal("5.0"),
        polygon=valid_polygon,
    )


@pytest.fixture
def point_inside():
    return OrderPoint(
        address="Тест", coordinates=Coordinates(latitude=55.7, longitude=37.5)
    )


@pytest.fixture
def point_outside():
    return OrderPoint(
        address="Тест", coordinates=Coordinates(latitude=56.0, longitude=38.0)
    )


class TestCityInitializatuin:
    def test_valid_city_creation(self, moscow_city: City):
        assert moscow_city.name == "Москва"
        assert moscow_city.state == "Московская область"
        assert moscow_city.base_price == Decimal("100.0")
        assert moscow_city.price_per_kilometer == Decimal("10.0")
        assert moscow_city.service_commission_pct == Decimal("5.0")
        assert moscow_city.polygon.is_valid

    def test_invalid_polygon_raises_exception(self, invalid_polygon):
        with pytest.raises(InvalidPolygon):
            City(
                name="Invalid City",
                state="Invalid State",
                base_price=Decimal("100.0"),
                price_per_kilometer=Decimal("10.0"),
                service_commission_pct=Decimal("5.0"),
                polygon=invalid_polygon,
            )


class TestPointInside:
    def test_point_inside(self, moscow_city: City, point_inside):
        assert moscow_city.is_point_inside(point=point_inside) is True

    def test_point_outside(self, moscow_city: City, point_outside):
        assert moscow_city.is_point_inside(point=point_outside) is False

    def test_point_on_boundary(self, moscow_city: City):
        boundary_point = OrderPoint(
            address="ТЕСТ", coordinates=Coordinates(latitude=55.5, longitude=37.5)
        )
        assert moscow_city.is_point_inside(boundary_point) is False


class TestRouteInside:
    def test_route_inside(self, moscow_city: City):
        points = [
            OrderPoint(
                address="Тест1", coordinates=Coordinates(latitude=55.6, longitude=37.4)
            ),
            OrderPoint(
                address="Тест2", coordinates=Coordinates(latitude=55.7, longitude=37.5)
            ),
            OrderPoint(
                address="Тест3", coordinates=Coordinates(latitude=55.8, longitude=37.6)
            ),
        ]
        assert moscow_city.is_route_inside(points) is True

    def test_route_partially_outside(self, moscow_city, point_outside):
        points = [
            OrderPoint(
                address="Тест", coordinates=Coordinates(latitude=55.7, longitude=37.5)
            ),
            point_outside,
        ]
        assert moscow_city.is_route_inside(points) is False

    def test_empty_route(self, moscow_city):
        assert moscow_city.is_route_inside([]) is False


class TestCityGeometry:
    def test_get_center(self, moscow_city: City):
        center = moscow_city.get_center()
        assert isinstance(center, tuple)
        assert len(center) == 2
        assert 55.5 <= center[0] <= 55.9
        assert 37.3 <= center[1] <= 37.8

    def test_intersects_with_same_city(self, moscow_city: City):
        assert moscow_city.intersects_with(moscow_city) is True

    def test_intersects_with_different_city(self, moscow_city: City):
        spb_polygon = Polygon(
            [(59.8, 30.1), (59.8, 30.5), (60.1, 30.5), (60.1, 30.1), (59.8, 30.1)]
        )
        spb_city = City(
            name="Санкт-Петербург",
            state="Ленинградская область",
            base_price=Decimal("120.0"),
            price_per_kilometer=Decimal("12.0"),
            service_commission_pct=Decimal("5.0"),
            polygon=spb_polygon,
        )
        assert moscow_city.intersects_with(spb_city) is False
