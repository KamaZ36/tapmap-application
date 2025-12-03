from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.api.services.auth.authorization import AuthorizationService


bearer_schema = HTTPBearer(auto_error=True)


def get_jwt_token_auth(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_schema),
) -> UUID:
    token = credentials.credentials
    token_data = AuthorizationService.get_token_data(token)
    return token_data


CurrentUserId = Annotated[UUID, Depends(get_jwt_token_auth)]
