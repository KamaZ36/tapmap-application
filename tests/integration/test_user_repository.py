import pytest
from uuid import uuid4

from app.infrastructure.repositories.user.sqlalchemy_repository import (
    SQLAlchemyUserRepository,
)
from app.domain.entities.user import User
from app.domain.value_objects.phone_number import PhoneNumber
from app.domain.enums.user import UserRole


@pytest.mark.integration
class TestUserRepositoryIntegration:
    @pytest.fixture
    async def user_repository(self, test_session):
        return SQLAlchemyUserRepository(test_session)

    @pytest.mark.asyncio
    async def test_create_and_get_user(self, user_repository: SQLAlchemyUserRepository):
        """Тест создания и получения пользователя через реальную БД"""
        # Arrange
        user = User(
            id=uuid4(),
            name="Integration Test User",
            phone_number=PhoneNumber("79999999999"),
            role=UserRole.USER,
        )

        # Act
        await user_repository.create(user)
        retrieved_user = await user_repository.get_by_id(user.id)

        # Assert
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        assert retrieved_user.name == user.name
        assert retrieved_user.phone_number.value == user.phone_number.value
        assert retrieved_user.role == user.role

    @pytest.mark.asyncio
    async def test_get_by_phone_number(self, user_repository: SQLAlchemyUserRepository):
        """Тест поиска пользователя по номеру телефона"""
        # Arrange
        phone = "78888888888"
        user = User(
            id=uuid4(),
            name="Phone Test User",
            phone_number=PhoneNumber(phone),
            role=UserRole.USER,
        )
        await user_repository.create(user)

        # Act
        found_user = await user_repository.get_by_phone(PhoneNumber(phone))

        # Assert
        assert found_user is not None
        assert found_user.phone_number.value == phone
