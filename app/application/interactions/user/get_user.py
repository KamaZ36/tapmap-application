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
    
    async def __call__(self, current_user: CurrentUser, get_user_id: UUID) -> User:
        self.validate_permissions(current_user=current_user, get_user_id=get_user_id)
        user = await self.user_repository.get_by_id(get_user_id)
        if not user: 
            raise UserNotFound()    
        return user

    def validate_permissions(self, current_user: CurrentUser, get_user_id: UUID) -> None:
        if UserRole.admin in current_user.roles:
            return 
        raise NoAccess()
    