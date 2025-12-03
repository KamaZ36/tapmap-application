import pytest
from uuid import uuid4

from app.application.queries.user.get_by_id import GetUserByIdQueryHandler
from app.application.dtos.user import CurrentUser
from app.domain.entities.user import User, UserRole
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.repositories.user.base import BaseUserRepository


@pytest.mark.asyncio
async def test_get_user_interactor_success(user_repository: BaseUserRepository):
    # Arrange
    user_id = uuid4()
    user = User(
        id=user_id,
        name="Test User",
        phone_number=PhoneNumber("79999999999"),
        role=UserRole.USER,
    )
    await user_repository.create(user)

    current_user = CurrentUser(user_id=user_id, roles=[UserRole.USER])

    interactor = GetUserByIdQueryHandler(user_repository)

    # Act
    result = await interactor(current_user, user_id)

    # Assert
    assert result == user


@pytest.mark.asyncio
async def test_get_user_interactor_admin_access(user_repository: BaseUserRepository):
    # Arrange
    user_id = uuid4()
    user = User(
        id=user_id,
        name="Test User",
        phone_number=PhoneNumber("79999999999"),
        role=UserRole.USER,
    )
    await user_repository.create(user)

    current_user = CurrentUser(
        user_id=uuid4(),  # Different user
        roles=[UserRole.ADMIN],
    )

    interactor = GetUserByIdQueryHandler(user_repository)

    # Act
    result = await interactor(current_user, user_id)

    # Assert
    assert result == user


@pytest.mark.asyncio
async def test_get_user_interactor_no_access(user_repository: BaseUserRepository):
    # Arrange
    user_id = uuid4()
    user = User(
        id=user_id,
        name="Test User",
        phone_number=PhoneNumber("79999999999"),
        role=UserRole.USER,
    )
    await user_repository.create(user)

    current_user = CurrentUser(
        user_id=uuid4(),  # Different user
        roles=[UserRole.USER],  # Not admin
    )

    interactor = GetUserByIdQueryHandler(user_repository)

    # Act & Assert
    from app.application.exceptions.permission import NoAccess

    with pytest.raises(NoAccess):
        await interactor(current_user, user_id)
