from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from app.application.commands.city import CreateCityCommand
from app.application.interactions.city.create import CreateCityInteraction

from app.presentation.api.dependencies import CurrentUserDep
from app.presentation.api.v1.schemas.city import CreateCitySchema


router = APIRouter(route_class=DishkaRoute)


@router.post(
    "",
    summary="Добавить новый город в поддерживаемые сервисом (Только администраторам)",
)
async def add_city(
    data: CreateCitySchema,
    current_user: CurrentUserDep,
    interactor: FromDishka[CreateCityInteraction],
) -> None:
    command = CreateCityCommand(**data.model_dump())
    city = await interactor(command=command, current_user=current_user)
