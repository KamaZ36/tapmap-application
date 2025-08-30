import pytest

from app.domain.entities.user import User
from app.application.interactions.user.create_user import CreateUserInteraction
from app.presentation.bots.user_tg_bot.schemas.user import CreateUserSchema
from tests.unit.repositories.fake_unit_of_work import FakeUnitOfWork


@pytest.mark.asyncio
async def test_create_user_interactor_success(fake_uow: FakeUnitOfWork):
    interactor = CreateUserInteraction(fake_uow)
    test_data = CreateUserSchema(
        name="Test User",
        phone_number="79999999999"
    )
    result = await interactor(test_data)
    
    assert isinstance(result, User)
    assert result.name == "Test User"
    assert result.phone_number.value == "79999999999"
    
    user_in_repo = await fake_uow.users.get_by_id(result.id)
    assert user_in_repo == result
    
    assert fake_uow.committed
    
@pytest.mark.asyncio
async def test_create_user_interactor_with_invalid_phone(fake_uow: FakeUnitOfWork):
    interactor = CreateUserInteraction(fake_uow)
    
    test_data = CreateUserSchema(
        name="Test User",
        phone_number="invalid_phone"
    )
    
    with pytest.raises(ValueError):
        await interactor(test_data)
