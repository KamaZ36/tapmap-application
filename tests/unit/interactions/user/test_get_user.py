import pytest
from uuid import uuid4

from app.application.queries.user.get_by_id import (
    GetUserByIdQuery,
    GetUserByIdQueryHandler,
)
from app.domain.entities.user import User
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.readers.user.base import BaseUserReader
from app.infrastructure.repositories.user.base import BaseUserRepository


@pytest.mark.asyncio
async def test_get_user_interactor_success(
    user_reader: BaseUserReader, user_repository: BaseUserRepository
):
    # Arrange
    user_id = uuid4()
    current_user_id = uuid4()

    user = User(
        id=user_id,
        name="Test User",
        phone_number=PhoneNumber("79999999999"),
    )
    await user_repository.create(user)

    query = GetUserByIdQuery(user_id=user_id, current_user_id=current_user_id)
    interactor = GetUserByIdQueryHandler(user_reader=user_reader)

    # Act
    result = await interactor(query)

    # Assert
    assert result.id == user.id
    assert result.name == user.name


@pytest.mark.asyncio
async def test_get_user_interactor_not_found(user_reader: BaseUserReader):
    # Arrange
    user_id = uuid4()
    current_user_id = uuid4()

    query = GetUserByIdQuery(user_id=user_id, current_user_id=current_user_id)
    interactor = GetUserByIdQueryHandler(user_reader=user_reader)

    # Act & Assert
    from app.application.exceptions.user import UserNotFound

    with pytest.raises(UserNotFound):
        await interactor(query)
