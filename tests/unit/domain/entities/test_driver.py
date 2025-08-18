import pytest

from app.domain.exceptions.driver import DriverAlreadyOnOrder, DriverAlreadyOnShift, DriverIsNotOrder, DriverIsNotShift
from uuid import UUID
from app.domain.utils.uuid_v7 import uuid7
from app.domain.entities.driver import Driver
from app.domain.value_objects.phone_number import PhoneNumber


def _create_driver(vehicle_id: UUID = uuid7()) -> Driver: 
    driver = Driver(
        first_name="Виктор",
        last_name="Викторович",
        phone_number=PhoneNumber('79999999999'),
    )
    return driver

def test_create_driver() -> None:
    vehicle_id = uuid7()
    driver = _create_driver(vehicle_id)
    assert driver.first_name == "Виктор"
    assert driver.last_name == "Викторович"
    assert driver.phone_number.value == "79999999999"
    assert driver.completed_orders_count == 0
    assert driver.cancelled_orders_count == 0
    assert driver.on_order == False
    assert driver.on_shift == False
    
def test_go_to_shift_driver() -> None: 
    driver = _create_driver()
    assert driver.on_shift == False
    driver.start_shift()
    assert driver.on_shift == True

def test_go_to_shift_driver_error() -> None: 
    driver = _create_driver()
    assert driver.on_shift == False
    driver.start_shift()
    assert driver.on_shift == True
    with pytest.raises(DriverAlreadyOnShift) as exc_info:
        driver.start_shift()
    
def test_leave_the_shift_driver() -> None: 
    driver = _create_driver()
    driver.start_shift()
    assert driver.on_shift == True
    driver.end_shift()
    assert driver.on_shift == False

def test_leave_the_shift_driver_error() -> None: 
    driver = _create_driver()
    driver.start_shift()
    assert driver.on_shift == True
    driver.end_shift()
    assert driver.on_shift == False
    with pytest.raises(DriverIsNotShift) as exc_info: 
        driver.end_shift()
        
def test_driver_assign_to_order() -> None: 
    driver = _create_driver()
    driver.start_shift()
    assert driver.on_order == False
    driver.assign_to_order()
    assert driver.on_order == True
    
def test_driver_assign_to_order_error_driver_is_not_shift() -> None: 
    driver = _create_driver()
    assert driver.on_order == False
    with pytest.raises(DriverIsNotShift): 
        driver.assign_to_order()
    
def test_driver_assign_to_order_error_driver_already_on_order() -> None: 
    driver = _create_driver()
    driver.start_shift()
    assert driver.on_order == False
    driver.assign_to_order()
    assert driver.on_order == True
    with pytest.raises(DriverAlreadyOnOrder): 
        driver.assign_to_order()

def test_driver_complete_order() -> None: 
    driver = _create_driver()
    driver.start_shift()
    driver.assign_to_order()
    assert driver.completed_orders_count == 0
    assert driver.on_order == True
    driver.complete_order()
    assert driver.on_order == False
    assert driver.completed_orders_count == 1

def test_driver_complete_order_error_driver_is_not_order() -> None: 
    driver = _create_driver()
    driver.start_shift()
    assert driver.completed_orders_count == 0
    assert driver.on_order == False
    with pytest.raises(DriverIsNotOrder):
        driver.complete_order()

def test_driver_cancel_order() -> None: 
    driver = _create_driver()
    driver.start_shift()
    driver.assign_to_order()
    assert driver.cancelled_orders_count == 0
    assert driver.on_order == True
    driver.cancel_order()
    assert driver.on_order == False
    assert driver.cancelled_orders_count == 1

def test_driver_cancel_order_error_driver_is_not_order() -> None: 
    driver = _create_driver()
    driver.start_shift()
    assert driver.cancelled_orders_count == 0
    assert driver.on_order == False
    with pytest.raises(DriverIsNotOrder):
        driver.cancel_order()
