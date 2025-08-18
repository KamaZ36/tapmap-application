from uuid import UUID
from app.domain.entities.user import UserRole
from app.services.exceptions.auth import NoAccess
from app.utils.jwt_service import jwt_service
from app.application.dtos.user import CurrentUser


class AuthorizationService:
    
    @staticmethod
    def get_token_data(access_token: str) -> CurrentUser:
        token_data = jwt_service.decode_access_token(access_token)
        current_user = CurrentUser(
            user_id=UUID(token_data['user_id']),
            roles=token_data['roles']
        )
        return current_user
    