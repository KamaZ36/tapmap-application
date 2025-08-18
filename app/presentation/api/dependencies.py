from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.application.dtos.user import CurrentUser
from app.infrastructure.database.connection import get_session
from app.presentation.api.v1.schemas.user import CurrentUserSchema
from app.services.authorization import AuthorizationService

from app.infrastructure.unit_of_work.base import BaseUnitOfWork
from app.infrastructure.unit_of_work.unit_of_work import UnitOfWork

bearer_schema = HTTPBearer(auto_error=True)

def get_jwt_token_auth(credentials: HTTPAuthorizationCredentials = Depends(bearer_schema)) -> CurrentUserSchema:
    token = credentials.credentials
    token_data = AuthorizationService.get_token_data(token)
    return token_data

CurrentUserDep = Annotated[CurrentUser, Depends(get_jwt_token_auth)]

def get_unit_of_work(session = Depends(get_session)) -> BaseUnitOfWork:
    return UnitOfWork(session)

UOW = Annotated[BaseUnitOfWork, Depends(get_unit_of_work)]
