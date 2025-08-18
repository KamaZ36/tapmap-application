import pytest

from app.application.interactions.user.get_user import GetUserInteractor
from tests.unit.repositories.fake_unit_of_work import FakeUnitOfWork


@pytest.mark.asyncio
async def test_get_user_interactor(fake_uow: FakeUnitOfWork):
    
    interactor = GetUserInteractor(fake_uow)
