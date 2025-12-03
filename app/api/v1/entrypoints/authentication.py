from fastapi import APIRouter

from app.api.services.auth.authentication import AuthenticationService

from app.api.v1.schemas.auth import (
    LoginSchema,
    RefreshLoginSchema,
    ResponseTokensSchema,
)
from app.core.dependencies import container


router = APIRouter()


@router.post("/login", summary="Аутентификация пользователя")
async def login_user(data: LoginSchema) -> ResponseTokensSchema:
    async with container() as req_conatiner:
        auth_service = await req_conatiner.get(AuthenticationService)
        tokens = await auth_service.login(data.phone_number)

    return ResponseTokensSchema.model_validate(tokens)


@router.post("/refresh", summary="Аутентификация пользователя")
async def refresh(data: RefreshLoginSchema) -> ResponseTokensSchema:
    async with container() as req_container:
        auth_service = await req_container.get(AuthenticationService)
        tokens = await auth_service.refresh(data.refresh_token)

    return ResponseTokensSchema.model_validate(tokens)
