from app.application.dtos.user import UserBlockingDTO, UserDTO
from app.infrastructure.database.models.user import BlockingUserModel, UserModel


def convert_user_to_dto(
    user_model: UserModel, user_blocking_model: BlockingUserModel | None = None
) -> UserDTO:
    user_blocking_dto = None

    if user_blocking_model:
        user_blocking_dto = UserBlockingDTO(
            id=user_blocking_model.id,
            user_id=user_blocking_model.user_id,
            reason=user_blocking_model.reason,
            expires_at=user_blocking_model.expires_at,
            created_at=user_blocking_model.created_at,
        )

    user_dto = UserDTO(
        id=user_model.id,
        name=user_model.name,
        phone_number=user_model.phone_number,
        status=user_model.status,
        completed_orders_count=user_model.completed_orders_count,
        cancelled_orders_count=user_model.cancelled_orders_count,
        base_city_id=user_model.base_city_id,
        roles=user_model.roles,
        created_at=user_model.created_at,
        blocking=user_blocking_dto,
    )
    return user_dto
