from dataclasses import dataclass
from typing import Any

from app.application.dtos.user import CurrentUser, GetUsersFilters
from app.application.exceptions.permission import NoAccess
from app.domain.entities.user import User
from app.domain.enums.user_role import UserRole
from app.infrastructure.repositories.user.base import BaseUserRepository


@dataclass
class GetUsersInteraction:
    user_repository: BaseUserRepository
    
    async def __call__(self, current_user: CurrentUser, filters: GetUsersFilters) -> list[User]:
        self._validate_permissions(current_user=current_user)
        users = await self.user_repository.get_filtered_users(filters=filters)
        return users
    
    def _validate_permissions(self, current_user: CurrentUser) -> None:
        if UserRole.admin in current_user.roles:
            return
        raise NoAccess()        
