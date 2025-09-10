import pytest

from app.domain.entities.user import User
from app.application.interactions.user.create_user import CreateUserInteraction
from app.application.commands.user import CreateUserCommand
from app.infrastructure.repositories.user.base import BaseUserRepository
from tests.unit.repositories.fake_transaction_manager import FakeTransactionManager


@pytest.mark.asyncio
async def test_create_user_interactor_success(
    user_repository: BaseUserRepository, transaction_manager: FakeTransactionManager
):
    interactor = CreateUserInteraction(user_repository, transaction_manager)

    test_data = CreateUserCommand(name="Test User", phone_number="79999999999")

    result = await interactor(test_data)

    assert isinstance(result, User)
    assert result.name == "Test User"
    assert result.phone_number.value == "79999999999"

    user_in_repo = await user_repository.get_by_id(result.id)
    assert user_in_repo == result

    assert transaction_manager.committed


@pytest.mark.asyncio
async def test_create_user_interactor_with_invalid_phone(
    user_repository: BaseUserRepository, transaction_manager: FakeTransactionManager
):
    interactor = CreateUserInteraction(user_repository, transaction_manager)

    test_data = CreateUserCommand(name="Test User", phone_number="invalid_phone")

    with pytest.raises(ValueError):
        await interactor(test_data)
