from functools import lru_cache

from app.application.commands.city.create import (
    CreateCityCommand,
    CreateCityInteraction,
)
from app.application.commands.driver.create import (
    CreateDriverCommand,
    CreateDriverCommandHandler,
)
from app.application.commands.driver.exit_from_shift import (
    DriverExitFromShiftCommand,
    DriverExitFromShiftCommandHandler,
)
from app.application.commands.driver.go_to_shift import (
    DriverGoToShiftCommand,
    DriverGoToShiftCommandHandler,
)
from app.application.commands.driver.update_location import (
    UpdateDriverLocationCommand,
    UpdateDriverLocationCommandHandler,
)
from app.application.commands.order.create import (
    CreateOrderCommand,
    CreateOrderCommandHandler,
)
from app.application.commands.order.update_status import (
    UpdateOrderStatusCommand,
    UpdateOrderStatusCommandHandler,
)
from app.application.commands.user.block import (
    BlockUserCommand,
    BlockUserCommandHandler,
)
from app.application.commands.user.unblock import (
    UnblockUserCommand,
    UnblockUserCommandHandler,
)

from app.application.commands.order.add_comment import (
    AddCommentToOrderCommand,
    AddCommentToOrderCommandHandler,
)
from app.application.commands.order.add_point import (
    AddPointToOrderCommand,
    AddPointToOrderCommandHandler,
)
from app.application.commands.order.cancel_order import (
    CancelOrderCommand,
    CancelOrderCommandHandler,
)
from app.application.commands.order.confirm import (
    ConfirmOrderCommand,
    ConfirmOrderCommandHandler,
)
from app.application.commands.user.create_user import (
    CreateUserCommand,
    CreateUserCommandHandler,
)
from app.application.queries.driver.get_by_id import (
    GetDriverByIdQuery,
    GetDriverByIdQueryHandler,
)
from app.application.queries.order.get_active_for_customer import (
    GetActiveOrderForCustomerQuery,
    GetActiveOrderForCustomerQueryHandler,
)
from app.application.queries.order.get_active_for_driver import (
    GetActiveOrderForDirverQuery,
    GetActiveOrderForDriverQueryHandler,
)
from app.application.queries.order.get_order_by_id import (
    GetOrderByIdQuery,
    GetOrderByIdQueryHandler,
)
from app.application.queries.order.get_orders import (
    GetOrdersListQuery,
    GetOrdersListQueryHandler,
)
from app.application.queries.user.get_by_id import (
    GetUserByIdQuery,
    GetUserByIdQueryHandler,
)
from app.application.queries.user.get_by_phone_number import (
    GetUserByPhoneQuery,
    GetUserByPhoneQueryHandler,
)
from app.core.mediator.mediator import Mediator


@lru_cache(1)
def get_mediator() -> Mediator:
    mediator = Mediator()

    # USER
    mediator.register_command(CreateUserCommand, CreateUserCommandHandler)
    mediator.register_command(BlockUserCommand, BlockUserCommandHandler)
    mediator.register_command(UnblockUserCommand, UnblockUserCommandHandler)

    mediator.register_query(GetUserByIdQuery, GetUserByIdQueryHandler)
    mediator.register_query(GetUserByPhoneQuery, GetUserByPhoneQueryHandler)

    # DRIVER
    mediator.register_command(CreateDriverCommand, CreateDriverCommandHandler)
    mediator.register_command(
        DriverExitFromShiftCommand, DriverExitFromShiftCommandHandler
    )
    mediator.register_command(DriverGoToShiftCommand, DriverGoToShiftCommandHandler)
    mediator.register_command(
        UpdateDriverLocationCommand, UpdateDriverLocationCommandHandler
    )

    mediator.register_query(GetDriverByIdQuery, GetDriverByIdQueryHandler)

    # ORDER
    mediator.register_command(CreateOrderCommand, CreateOrderCommandHandler)
    mediator.register_command(AddPointToOrderCommand, AddPointToOrderCommandHandler)
    mediator.register_command(AddCommentToOrderCommand, AddCommentToOrderCommandHandler)
    mediator.register_command(ConfirmOrderCommand, ConfirmOrderCommandHandler)
    mediator.register_command(UpdateOrderStatusCommand, UpdateOrderStatusCommandHandler)
    mediator.register_command(CancelOrderCommand, CancelOrderCommandHandler)

    mediator.register_query(GetOrderByIdQuery, GetOrderByIdQueryHandler)
    mediator.register_query(
        GetActiveOrderForCustomerQuery, GetActiveOrderForCustomerQueryHandler
    )
    mediator.register_query(
        GetActiveOrderForDirverQuery, GetActiveOrderForDriverQueryHandler
    )
    mediator.register_query(GetOrdersListQuery, GetOrdersListQueryHandler)

    # CITY
    mediator.register_command(CreateCityCommand, CreateCityInteraction)

    return mediator
