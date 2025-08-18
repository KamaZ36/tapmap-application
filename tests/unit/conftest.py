import pytest

from app.domain.entities.driver import Driver
from app.domain.entities.vehicle import Vehicle
from app.domain.utils.uuid_v7 import uuid7
from app.domain.value_objects.phone_number import PhoneNumber
from app.domain.value_objects.vehicle_number import VehicleNumber


@pytest.fixture
def test_driver() -> Driver:
    return Driver(
        first_name="Виктор",
        last_name="Викторович",
        phone_number=PhoneNumber('79999999999'),
    )

@pytest.fixture
def vehicle():
    return Vehicle(
        driver_id=uuid7(),
        brand="Toyota",
        model="Camry",
        color="черный",
        number=VehicleNumber("К123КК36")
    )
    