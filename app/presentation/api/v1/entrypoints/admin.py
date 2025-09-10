from uuid import UUID
from fastapi import APIRouter

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from app.domain.entities.user import User
from app.application.interactions.driver.get_driver import GetDriverInteraction
from app.application.interactions.user.get_user import GetUserInteractor
from app.presentation.api.dependencies import CurrentUserDep
from app.presentation.api.v1.schemas.driver import ResponseDriverSchema
from app.presentation.api.v1.schemas.user import ResponseUserSchema


router = APIRouter(route_class=DishkaRoute)


@router.get("/users/{user_id}", summary="Получить пользователя по ID")
async def admin_get_user_by_id(
    user_id: UUID,
    current_user: CurrentUserDep,
    interactor: FromDishka[GetUserInteractor],
) -> ResponseUserSchema:
    user = await interactor(current_user=current_user, user_id=user_id)
    return ResponseUserSchema.from_domain(user)


@router.get("/drivers/{driver_id}", summary="Получить водителя по ID")
async def admin_get_driver_by_id(
    driver_id: UUID,
    current_user: CurrentUserDep,
    interactor: FromDishka[GetDriverInteraction],
) -> ResponseDriverSchema:
    driver = await interactor(current_user=current_user, driver_id=driver_id)
    return ResponseDriverSchema.from_domain(driver)
