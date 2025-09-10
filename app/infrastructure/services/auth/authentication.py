from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions.user import UserNotFound
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.repositories.user.base import BaseUserRepository

from app.infrastructure.services.jwt_service import jwt_service


@dataclass
class AuthenticationService:
    user_repository: BaseUserRepository

    async def login(self, phone_number: str) -> dict[str, str] | None:
        phone = PhoneNumber(phone_number)
        user = await self.user_repository.get_by_phone(phone.value)
        if user is None:
            raise UserNotFound()
        tokens = jwt_service.create_tokens(user_id=user.id, roles=user.roles)
        return tokens

    async def refresh(self, refresh_token: str) -> dict[str, str] | None:
        token_data = jwt_service.decode_refresh_token(refresh_token)
        user = await self.user_repository.get_by_id(UUID(token_data["user_id"]))
        if user is None:
            raise UserNotFound()
        tokens = jwt_service.create_tokens(user_id=user.id, roles=user.roles)
        return tokens
