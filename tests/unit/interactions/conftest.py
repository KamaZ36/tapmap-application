import pytest

from tests.unit.repositories.fake_unit_of_work import FakeUnitOfWork


@pytest.fixture(scope='session')
def fake_uow():
    return FakeUnitOfWork()
