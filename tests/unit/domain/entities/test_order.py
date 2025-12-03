import pytest

from decimal import Decimal
from app.domain.exceptions.order import (
    DriverAlreadyAssignedToOrder,
    InvalidOrderStatusTransition,
    OrderCannotTwoPoints,
)
from app.utils.uuid_v7 import uuid7
from app.domain.entities.order import Order, OrderStatus
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.money import Money
from app.domain.value_objects.order_point import OrderPoint


def _create_points() -> list[OrderPoint]:
    point1 = OrderPoint(
        address="Москва, Красная площадь, 1",
        coordinates=Coordinates(latitude=55.7539, longitude=37.6208),
    )
    point2 = OrderPoint(
        address="Санкт-Петербург, Невский проспект, 1",
        coordinates=Coordinates(latitude=59.9343, longitude=30.3351),
    )
    return [point1, point2]


@pytest.fixture
def sample_order():
    points = _create_points()
    return Order(
        customer_id=uuid7(),
        city_id=uuid7(),
        points=points,
        price=Money(Decimal(100)),
        service_commission=Money(Decimal(10)),
        travel_distance=1000,
        travel_time=10,
    )


class TestOrderInitialization:
    def test_order_creation_with_minimum_points(self):
        """Тест создания заказа с минимальным количеством точек"""
        points = _create_points()
        order = Order(
            customer_id=uuid7(),
            city_id=uuid7(),
            points=points,
            price=Money(1000),
            service_commission=Money(100),
            travel_distance=1000,
            travel_time=10,
        )
        assert order.status == OrderStatus.driver_search

    def test_order_creation_with_less_than_two_points_error(self):
        with pytest.raises(OrderCannotTwoPoints):
            Order(
                customer_id=uuid7(),
                city_id=uuid7(),
                points=[
                    OrderPoint(
                        address="Тест",
                        coordinates=Coordinates(latitude=51.23, longitude=41.23),
                    )
                ],
                price=Money(1000),
                service_commission=Money(100),
                travel_distance=1000,
                travel_time=10,
            )


class TestOrderStatusTranzitions:
    def test_initial_status(self, sample_order: Order):
        """Тест начального статуса заказа"""
        assert sample_order.status == OrderStatus.driver_search

    def test_assign_driver_success(self, sample_order: Order):
        """Тест успешного назначения водителя на заказ"""
        driver_id = uuid7()
        sample_order.assign_driver(driver_id, feeding_distance=1000, feeding_time=10)
        assert sample_order.driver_id == driver_id
        assert sample_order.status == OrderStatus.waiting_driver

    def test_cancel_order(self, sample_order: Order):
        """Тест отмены заказа"""
        sample_order.cancel()
        assert sample_order.status == OrderStatus.cancelled

    def test_cancel_completed_order_error(self, sample_order: Order):
        """Тест нельзя отменить завершенный заказ"""
        driver_id = uuid7()
        sample_order.assign_driver(driver_id, feeding_distance=1000, feeding_time=10)
        sample_order.status = OrderStatus.completed
        with pytest.raises(InvalidOrderStatusTransition):
            sample_order.cancel()

    def test_status_transitions_sequence(self, sample_order: Order):
        driver_id = uuid7()
        sample_order.assign_driver(driver_id, feeding_distance=1000, feeding_time=10)
        assert sample_order.status == OrderStatus.waiting_driver

        sample_order.update_status()
        assert sample_order.status == OrderStatus.driver_waiting_customer

        sample_order.update_status()
        assert sample_order.status == OrderStatus.processing

        sample_order.update_status()
        assert sample_order.status == OrderStatus.completed

        with pytest.raises(InvalidOrderStatusTransition):
            sample_order.update_status()


class TestEdgeCases:
    def test_update_status_without_driver_fails(self, sample_order):
        """Тест: нельзя перевести в waiting_driver без водителя"""
        sample_order.status = OrderStatus.driver_search
        with pytest.raises(InvalidOrderStatusTransition):
            sample_order.update_status()

    def test_get_next_status_for_terminal_statuses(self, sample_order):
        """Тест: терминальные статусы не имеют следующего статуса"""
        sample_order.status = OrderStatus.completed
        assert sample_order._get_next_status() is None

        sample_order.status = OrderStatus.cancelled
        assert sample_order._get_next_status() is None

    def test_assign_driver_in_invalid_status_fails(self, sample_order):
        """Тест: нельзя назначить водителя в невалидном статусе"""
        # Сначала назначим водителя в валидном статусе
        driver_id = uuid7()
        sample_order.assign_driver(driver_id, 1000, 10)

        # Теперь попробуем назначить другого водителя - должно вызвать исключение
        with pytest.raises(DriverAlreadyAssignedToOrder):
            sample_order.assign_driver(uuid7(), 1000, 10)
