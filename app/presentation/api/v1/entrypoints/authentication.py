from fastapi import APIRouter

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from app.infrastructure.services.auth.authentication import AuthenticationService

from app.presentation.api.v1.schemas.auth import (
    LoginSchema,
    RefreshLoginSchema,
    ResponseTokensSchema,
)


router = APIRouter(route_class=DishkaRoute)


@router.post("/tg_bot/login", summary="Аутентификация пользователя")
async def login_user(
    data: LoginSchema, auth_service: FromDishka[AuthenticationService]
) -> ResponseTokensSchema:
    tokens = await auth_service.login(data.phone_number)
    return ResponseTokensSchema.model_validate(tokens)


@router.post("/tg_bot/refresh", summary="Аутентификация пользователя")
async def refresh(
    data: RefreshLoginSchema, auth_service: FromDishka[AuthenticationService]
) -> ResponseTokensSchema:
    tokens = await auth_service.refresh(data.refresh_token)
    return ResponseTokensSchema.model_validate(tokens)
