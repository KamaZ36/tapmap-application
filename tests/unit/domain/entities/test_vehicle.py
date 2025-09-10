from uuid import uuid4
from app.domain.entities.vehicle import Vehicle
from app.domain.value_objects.vehicle_number import VehicleNumber


def _create_vehicle() -> Vehicle:
    return Vehicle(
        driver_id=uuid4(),
        brand="Toyota",
        model="Camry",
        color="черный",
        number=VehicleNumber("К123КК36"),
    )


def test_display_name():
    vehicle = _create_vehicle()
    name = vehicle.display_name()
    assert "Toyota" in name
    assert "Camry" in name
    assert "черный" in name
    assert "К123КК36" in name


def test_update_driver():
    vehicle = _create_vehicle()
    new_driver_id = uuid4()
    vehicle.update_driver(new_driver_id)
    assert vehicle.driver_id == new_driver_id


def test_repaint():
    vehicle = _create_vehicle()
    vehicle.repaint("Белый")
    assert vehicle.color == "Белый"


def test_update_number():
    vehicle = _create_vehicle()
    new_number = VehicleNumber("К777КК136")
    vehicle.update_number(new_number)
    assert vehicle.number == new_number
