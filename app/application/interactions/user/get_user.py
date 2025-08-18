from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.user import CurrentUser
from app.application.exceptions.permission import NoAccess
from app.application.exceptions.user import UserNotFound

from app.domain.entities.user import User, UserRole

from app.infrastructure.repositories.user.base import BaseUserRepository


@dataclass
class GetUserInteractor:
    user_repository: BaseUserRepository
    
    async def __call__(self, current_user: CurrentUser, user_id: UUID) -> User:
        if UserRole.admin not in current_user.roles and current_user.user_id != user_id:
            raise NoAccess()
        
        user = await self.user_repository.get_by_id(user_id)
        if not user: 
            raise UserNotFound()
        return user
    