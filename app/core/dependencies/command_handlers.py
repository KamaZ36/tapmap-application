from dishka import Provider, Scope, provide

from app.application.commands.driver.exit_from_shift import (
    DriverExitFromShiftCommandHandler,
)
from app.application.commands.driver.go_to_shift import DriverGoToShiftCommandHandler
from app.application.commands.order.add_comment import AddCommentToOrderCommandHandler
from app.application.commands.order.add_point import AddPointToOrderCommandHandler
from app.application.commands.order.confirm import ConfirmOrderCommandHandler
from app.application.commands.order.create import CreateOrderCommandHandler
from app.application.commands.user.block import BlockUserCommandHandler
from app.application.commands.user.create_user import CreateUserCommandHandler
from app.application.commands.user.unblock import UnblockUserCommandHandler


from app.application.commands.driver.create import CreateDriverCommandHandler

from app.application.commands.driver.update_location import (
    UpdateDriverLocationCommandHandler,
)

from app.application.commands.order.cancel_order import CancelOrderCommandHandler
from app.application.commands.order.process_order import ProcessOrderInteraction
from app.application.commands.order.update_status import (
    UpdateOrderStatusCommandHandler,
)

from app.application.commands.vehicle.create_vehicle import CreateVehicleInteraction


class CommandHandlersProvider(Provider):
    scope = Scope.REQUEST

    # USER
    create_user_interactor = provide(CreateUserCommandHandler)
    block_user_interactor = provide(BlockUserCommandHandler)
    unblock_user_interactor = provide(UnblockUserCommandHandler)

    # DRIVER
    create_driver_interactor = provide(CreateDriverCommandHandler)
    driver_go_to_shift_interactor = provide(DriverGoToShiftCommandHandler)
    driver_exit_from_shfit_interactor = provide(DriverExitFromShiftCommandHandler)
    update_location_interactor = provide(UpdateDriverLocationCommandHandler)

    # ORDERS
    create_order_interactor = provide(CreateOrderCommandHandler)
    add_point_to_order_interactor = provide(AddPointToOrderCommandHandler)
    add_comment_to_draft_order_interactor = provide(AddCommentToOrderCommandHandler)
    confirm_order_interactor = provide(ConfirmOrderCommandHandler)
    cancel_order_interactor = provide(CancelOrderCommandHandler)
    update_order_status_interactor = provide(UpdateOrderStatusCommandHandler)
    process_order_interactor = provide(ProcessOrderInteraction)

    # VEHICLES
    create_vehicle_interactor = provide(CreateVehicleInteraction)
