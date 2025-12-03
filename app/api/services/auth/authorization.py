from uuid import UUID

from app.domain.entities.user import UserRole

from app.api.services.jwt_service import jwt_service

from app.application.dtos.user import CurrentUser


class AuthorizationService:
    @staticmethod
    def get_token_data(access_token: str) -> UUID:
        token_data = jwt_service.decode_access_token(access_token)
        return UUID(token_data["user_id"])
