import pytest
from uuid import uuid4

from app.application.commands.driver.create import (
    CreateDriverCommand,
    CreateDriverCommandHandler,
)
from app.application.dtos.driver import DriverDTO
from app.application.exceptions.user import UserNotFound
from app.domain.entities.user import User
from app.domain.enums.user import UserRole
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.user.base import BaseUserRepository
from app.infrastructure.database.transaction_manager.base import TransactionManager
from tests.unit.repositories.fake_transaction_manager import FakeTransactionManager


@pytest.mark.asyncio
async def test_create_driver_interactor_success(
    driver_repository: BaseDriverRepository,
    user_repository: BaseUserRepository,
    transaction_manager: FakeTransactionManager,
):
    """Тест успешного создания водителя администратором"""
    # Arrange
    interactor = CreateDriverCommandHandler(
        driver_repository=driver_repository,
        user_repository=user_repository,
        transaction_manager=transaction_manager,
    )

    user_id = uuid4()
    test_user = User(
        id=user_id, name="Test User", phone_number=PhoneNumber("79999999999")
    )

    # Создаем пользователя в репозитории
    await user_repository.create(test_user)

    command = CreateDriverCommand(
        current_user_id=uuid4(),
        user_id=user_id,
        first_name="Иван",
        last_name="Иванов",
        middle_name="Иванович",
        license_number="1234567890",
        phone_number="79999999999",
    )

    # Act
    result = await interactor(command)

    # Assert
    assert isinstance(result, DriverDTO)
    assert result.id == user_id
    assert result.first_name == "Иван"
    assert result.last_name == "Иванов"
    assert result.middle_name == "Иванович"
    assert result.license_number == "1234567890"
    assert result.phone_number == "79999999999"
    assert result.completed_orders_count == 0
    assert result.cancelled_orders_count == 0
    assert result.status.value == "active"
    assert result.on_shift is False
    assert result.on_order is False

    # Проверяем, что водитель создан в репозитории
    driver_in_repo = await driver_repository.get_by_id(user_id)
    assert driver_in_repo is not None
    assert driver_in_repo.id == user_id

    # Проверяем, что пользователь обновлен с ролью водителя
    updated_user = await user_repository.get_by_id(user_id)
    assert UserRole.driver in updated_user.roles

    # Проверяем, что транзакция зафиксирована
    assert transaction_manager.committed


@pytest.mark.asyncio
async def test_create_driver_interactor_user_not_found(
    driver_repository: BaseDriverRepository,
    user_repository: BaseUserRepository,
    transaction_manager: FakeTransactionManager,
):
    """Тест создания водителя для несуществующего пользователя"""
    # Arrange
    interactor = CreateDriverCommandHandler(
        driver_repository=driver_repository,
        user_repository=user_repository,
        transaction_manager=transaction_manager,
    )

    non_existent_user_id = uuid4()

    command = CreateDriverCommand(
        current_user_id=uuid4(),
        user_id=non_existent_user_id,
        first_name="Иван",
        last_name="Иванов",
        middle_name="Иванович",
        license_number="1234567890",
        phone_number="79999999999",
    )

    # Act & Assert
    with pytest.raises(UserNotFound):
        await interactor(command)

    # Проверяем, что транзакция не была зафиксирована
    assert not transaction_manager.committed


@pytest.mark.asyncio
async def test_create_driver_interactor_without_middle_name(
    driver_repository: BaseDriverRepository,
    user_repository: BaseUserRepository,
    transaction_manager: FakeTransactionManager,
):
    """Тест создания водителя без отчества"""
    # Arrange
    interactor = CreateDriverCommandHandler(
        driver_repository=driver_repository,
        user_repository=user_repository,
        transaction_manager=transaction_manager,
    )

    user_id = uuid4()
    test_user = User(
        id=user_id, name="Test User", phone_number=PhoneNumber("79999999999")
    )

    await user_repository.create(test_user)

    command = CreateDriverCommand(
        current_user_id=uuid4(),
        user_id=user_id,
        first_name="Иван",
        last_name="Иванов",
        middle_name=None,  # Пустое отчество
        license_number="1234567890",
        phone_number="79999999999",
    )

    # Act
    result = await interactor(command)

    # Assert
    assert result.middle_name is None
    assert transaction_manager.committed


@pytest.mark.asyncio
async def test_create_driver_interactor_multiple_admin_roles(
    driver_repository: BaseDriverRepository,
    user_repository: BaseUserRepository,
    transaction_manager: FakeTransactionManager,
):
    """Тест создания водителя пользователем с несколькими ролями включая админа"""
    # Arrange
    interactor = CreateDriverCommandHandler(
        driver_repository=driver_repository,
        user_repository=user_repository,
        transaction_manager=transaction_manager,
    )

    user_id = uuid4()
    test_user = User(
        id=user_id, name="Test User", phone_number=PhoneNumber("79999999999")
    )

    await user_repository.create(test_user)

    command = CreateDriverCommand(
        current_user_id=uuid4(),
        user_id=user_id,
        first_name="Иван",
        last_name="Иванов",
        middle_name="Иванович",
        license_number="1234567890",
        phone_number="79999999999",
    )

    # Act
    result = await interactor(command)

    # Assert
    assert isinstance(result, DriverDTO)
    assert transaction_manager.committed
