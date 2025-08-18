from uuid import UUID
from app.infrastructure.unit_of_work.base import BaseUnitOfWork

from app.utils.jwt_service import jwt_service


class AuthenticationService:
    
    def __init__(self, uow: BaseUnitOfWork) -> None:
        self.uow = uow
    
    async def login(self, phone_number: str) -> dict[str, str] | None:
        user = await self.uow.users.get_by_phone(phone_number)
        tokens = jwt_service.create_tokens(user_id=user.id, roles=user.roles)
        return tokens
    
    async def refresh(self, refresh_token: str) -> dict[str, str] | None:
        token_data = jwt_service.decode_refresh_token(refresh_token)
        user = await self.uow.users.get_by_id(UUID(token_data['user_id']))
        tokens = jwt_service.create_tokens(user_id=user.id, roles=user.roles)
        return tokens
    