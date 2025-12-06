import pytest

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.city.base import BaseCityRepository
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository
from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.order.base import BaseOrderRepository
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.repositories.vehicle.base import BaseVehicleRepository

from tests.unit.repositories.fake_city_repository import FakeCityRepository
from tests.unit.repositories.fake_draft_order_repository import FakeDraftOrderRepository
from tests.unit.repositories.fake_driver_repository import FakeDriverRepository
from tests.unit.repositories.fake_order_repository import FakeOrderRepository
from tests.unit.repositories.fake_user_repository import FakeUserRepository
from tests.unit.repositories.fake_user_reader import FakeUserReader
from tests.unit.repositories.fake_vehicle_repository import FakeVehicleRepository
from tests.unit.repositories.fake_transaction_manager import FakeTransactionManager

from app.infrastructure.readers.user.base import BaseUserReader


@pytest.fixture(scope="function")
def transaction_manager() -> TransactionManager:
    return FakeTransactionManager()


@pytest.fixture(scope="function")
def user_repository() -> BaseUserRepository:
    return FakeUserRepository()


@pytest.fixture(scope="function")
def driver_repository() -> BaseDriverRepository:
    return FakeDriverRepository()


@pytest.fixture(scope="function")
def order_repository() -> BaseOrderRepository:
    return FakeOrderRepository()


@pytest.fixture(scope="function")
def city_repository() -> BaseCityRepository:
    return FakeCityRepository()


@pytest.fixture(scope="function")
def vehicle_repository() -> BaseVehicleRepository:
    return FakeVehicleRepository()


@pytest.fixture(scope="function")
def draft_order_repository() -> BaseDraftOrderRepository:
    return FakeDraftOrderRepository()


@pytest.fixture(scope="function")
def user_reader(user_repository: BaseUserRepository) -> BaseUserReader:
    return FakeUserReader(user_repository=user_repository)
