import pytest

from app.application.dtos.user import UserDTO
from app.application.commands.user.create_user import (
    CreateUserCommand,
    CreateUserCommandHandler,
)
from app.infrastructure.repositories.user.base import BaseUserRepository
from tests.unit.repositories.fake_transaction_manager import FakeTransactionManager


@pytest.mark.asyncio
async def test_create_user_interactor_success(
    user_repository: BaseUserRepository, transaction_manager: FakeTransactionManager
):
    interactor = CreateUserCommandHandler(user_repository, transaction_manager)

    test_data = CreateUserCommand(name="Test User", phone_number="79999999999")

    result = await interactor(test_data)

    assert isinstance(result, UserDTO)
    assert result.name == "Test User"
    assert result.phone_number == "79999999999"

    user_in_repo = await user_repository.get_by_id(result.id)
    assert user_in_repo is not None
    assert user_in_repo.name == "Test User"

    assert transaction_manager.committed


@pytest.mark.asyncio
async def test_create_user_interactor_with_invalid_phone(
    user_repository: BaseUserRepository, transaction_manager: FakeTransactionManager
):
    interactor = CreateUserCommandHandler(user_repository, transaction_manager)

    test_data = CreateUserCommand(name="Test User", phone_number="invalid_phone")

    from app.domain.exceptions.phone_number import InvalidPhoneNumber

    with pytest.raises(InvalidPhoneNumber):
        await interactor(test_data)
