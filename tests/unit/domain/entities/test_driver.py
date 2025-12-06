import pytest

from app.domain.exceptions.driver import (
    DriverAlreadyOnOrder,
    DriverAlreadyOnShift,
    DriverIsNotOrder,
    DriverIsNotShift,
)
from app.domain.entities.driver import Driver
from app.domain.value_objects.phone_number import PhoneNumber


def _create_driver() -> Driver:
    driver = Driver(
        first_name="Виктор",
        last_name="Викторович",
        phone_number=PhoneNumber("79999999999"),
        license_number="1234567890",
    )
    return driver


def test_create_driver() -> None:
    driver = _create_driver()
    assert driver.first_name == "Виктор"
    assert driver.last_name == "Викторович"
    assert driver.phone_number.value == "79999999999"
    assert driver.license_number == "1234567890"
    assert driver.completed_orders_count == 0
    assert driver.cancelled_orders_count == 0
    assert driver.on_order is False
    assert driver.on_shift is False
    assert driver.status.value == "active"


def test_go_to_shift_driver() -> None:
    driver = _create_driver()
    assert driver.on_shift is False
    driver.start_shift()
    assert driver.on_shift is True


def test_leave_the_shift_driver() -> None:
    driver = _create_driver()
    driver.start_shift()
    assert driver.on_shift is True
    driver.end_shift()
    assert driver.on_shift is False


def test_driver_assign_to_order() -> None:
    driver = _create_driver()
    driver.start_shift()
    assert driver.on_order is False
    driver.assign_to_order()
    assert driver.on_order is True


def test_driver_assign_to_order_error_driver_is_not_shift() -> None:
    driver = _create_driver()
    assert driver.on_order is False
    with pytest.raises(DriverIsNotShift):
        driver.assign_to_order()


def test_driver_assign_to_order_error_driver_already_on_order() -> None:
    driver = _create_driver()
    driver.start_shift()
    assert driver.on_order is False
    driver.assign_to_order()
    assert driver.on_order is True
    with pytest.raises(DriverAlreadyOnOrder):
        driver.assign_to_order()


def test_driver_complete_order() -> None:
    driver = _create_driver()
    driver.start_shift()
    driver.assign_to_order()
    assert driver.completed_orders_count == 0
    assert driver.on_order is True
    driver.complete_order()
    assert driver.on_order is False
    assert driver.completed_orders_count == 1


def test_driver_complete_order_error_driver_is_not_order() -> None:
    driver = _create_driver()
    driver.start_shift()
    assert driver.completed_orders_count == 0
    assert driver.on_order is False
    with pytest.raises(DriverIsNotOrder):
        driver.complete_order()


def test_driver_cancel_order() -> None:
    driver = _create_driver()
    driver.start_shift()
    driver.assign_to_order()
    assert driver.cancelled_orders_count == 0
    assert driver.on_order is True
    driver.cancel_order()
    assert driver.on_order is False
    assert driver.cancelled_orders_count == 1


def test_driver_cancel_order_error_driver_is_not_order() -> None:
    driver = _create_driver()
    driver.start_shift()
    assert driver.cancelled_orders_count == 0
    assert driver.on_order is False
    with pytest.raises(DriverIsNotOrder):
        driver.cancel_order()


def test_driver_update_location() -> None:
    driver = _create_driver()
    from app.domain.value_objects.coordinates import Coordinates

    coordinates = Coordinates(latitude=55.7558, longitude=37.6176)
    driver.update_location(coordinates)

    assert driver.last_location == coordinates
    assert driver.last_location.latitude == 55.7558
    assert driver.last_location.longitude == 37.6176
