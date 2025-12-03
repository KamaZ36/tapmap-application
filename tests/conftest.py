import pytest
from uuid import uuid4

from app.domain.entities.user import User
from app.domain.entities.driver import Driver
from app.domain.entities.vehicle import Vehicle
from app.domain.value_objects.phone_number import PhoneNumber
from app.domain.value_objects.vehicle_number import VehicleNumber
from app.domain.value_objects.coordinates import Coordinates
from app.domain.enums.user import UserRole


@pytest.fixture
def sample_phone_number() -> str:
    return "79999999999"


@pytest.fixture
def sample_coordinates() -> Coordinates:
    return Coordinates(latitude=55.7558, longitude=37.6176)


@pytest.fixture
def sample_user(sample_phone_number: str) -> User:
    return User(
        id=uuid4(),
        name="Test User",
        phone_number=PhoneNumber(sample_phone_number),
        role=UserRole.USER,
    )


@pytest.fixture
def sample_driver(sample_phone_number: str) -> Driver:
    return Driver(
        id=uuid4(),
        first_name="Виктор",
        last_name="Викторович",
        phone_number=PhoneNumber(sample_phone_number),
    )


@pytest.fixture
def sample_vehicle() -> Vehicle:
    return Vehicle(
        id=uuid4(),
        driver_id=uuid4(),
        brand="Toyota",
        model="Camry",
        color="черный",
        number=VehicleNumber("К123КК36"),
    )
