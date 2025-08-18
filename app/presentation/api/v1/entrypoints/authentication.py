from fastapi import APIRouter

from app.presentation.api.dependencies import UOW
from app.presentation.api.v1.schemas.auth import LoginSchema, RefreshLoginSchema, ResponseTokensSchema
from app.services.authentication import AuthenticationService


router = APIRouter()


@router.post(
    '/login',
    summary="Аутентификация пользователя"
)
async def login_user(
    data: LoginSchema,
    uow: UOW
) -> ResponseTokensSchema:
    auth_service = AuthenticationService(uow)
    tokens = await auth_service.login(data.phone_number)
    return ResponseTokensSchema.model_validate(tokens)

@router.post(
    '/refresh',
    summary="Аутентификация пользователя"
)
async def refresh(
    data: RefreshLoginSchema,
    uow: UOW
) -> ResponseTokensSchema:
    auth_service = AuthenticationService(uow)
    tokens = await auth_service.refresh(data.refresh_token)
    return ResponseTokensSchema.model_validate(tokens)
