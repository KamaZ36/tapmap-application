from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.application.dtos.user import CurrentUser

from app.infrastructure.services.auth.authorization import AuthorizationService

from app.presentation.api.v1.schemas.user import CurrentUserSchema


bearer_schema = HTTPBearer(auto_error=True)


def get_jwt_token_auth(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_schema),
) -> CurrentUserSchema:
    token = credentials.credentials
    token_data = AuthorizationService.get_token_data(token)
    return token_data


CurrentUserDep = Annotated[CurrentUser, Depends(get_jwt_token_auth)]
