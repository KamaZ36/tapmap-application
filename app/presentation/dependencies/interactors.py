from dishka import Provider, Scope, provide

from app.application.interactions.user.create_user import CreateUserInteraction
from app.application.interactions.user.get_active_order import GetActiveOrderForUserInteraction
from app.application.interactions.user.get_user import GetUserInteractor
from app.application.interactions.user.get_users import GetUsersInteraction
from app.application.interactions.user.set_base_location import SetBaseLocationUserInteraction

from app.application.interactions.driver.create_driver import CreateDriverInteraction
from app.application.interactions.driver.get_active_order import GetActiveOrderForDriverInteraction
from app.application.interactions.driver.get_driver import GetDriverInteraction
from app.application.interactions.driver.get_last_location import GetLastLocationDriverInteraction
from app.application.interactions.driver.switch_on_shift import SwitchDriverOnShiftInteraction
from app.application.interactions.driver.update_location import UpdateLocationInteraction

from app.application.interactions.draft_order.add_comment import AddCommentToDraftOrderInteraction
from app.application.interactions.draft_order.add_point import AddPointToDraftOrderInteraction
from app.application.interactions.draft_order.confirm_draft_order import ConfirmDraftOrderInteraction
from app.application.interactions.draft_order.create_order import CreateDraftOrderInteraction
from app.application.interactions.draft_order.delete import DeleteDraftOrderInteraction
from app.application.interactions.draft_order.get_draft_order import GetDraftOrderInteraction

from app.application.interactions.order.cancel_order import CancelOrderInteraction
from app.application.interactions.order.get_order import GetOrderInteraction
from app.application.interactions.order.get_orders import GetOrdersInteraction
from app.application.interactions.order.process_order import ProcessOrderInteraction
from app.application.interactions.order.update_status import UpdateStatusInteraction

from app.application.interactions.city.create import CreateCityInteraction

from app.application.interactions.vehicle.create_vehicle import CreateVehicleInteraction
from app.application.interactions.vehicle.get_vehicle import GetVehicleInteraction
from app.application.interactions.vehicle.get_vehicles import GetVehiclesInteraction


class Interactors(Provider):
    scope = Scope.REQUEST

    # USER
    get_user_interactor = provide(GetUserInteractor)
    get_active_order_for_user_interactor = provide(GetActiveOrderForUserInteraction)
    create_user_interactor = provide(CreateUserInteraction)
    get_users_interactor = provide(GetUsersInteraction)
    set_user_base_city_interactor = provide(SetBaseLocationUserInteraction)

    # DRIVER
    get_driver_interactor = provide(GetDriverInteraction)
    create_driver_interactor = provide(CreateDriverInteraction)
    update_location_interactor = provide(UpdateLocationInteraction)
    get_location_interactor = provide(GetLastLocationDriverInteraction)
    switch_on_shift_interactor = provide(SwitchDriverOnShiftInteraction)
    get_active_order_interactor = provide(GetActiveOrderForDriverInteraction)

    # ORDERS
    get_draft_order_interactor = provide(GetDraftOrderInteraction)
    get_orders_list_interactor = provide(GetOrdersInteraction)
    get_order_interactor = provide(GetOrderInteraction)
    create_order_interactor = provide(CreateDraftOrderInteraction)
    add_point_to_draft_order_interactor = provide(AddPointToDraftOrderInteraction)
    add_comment_to_draft_order_interactor = provide(AddCommentToDraftOrderInteraction)
    confirm_draft_order_interactor = provide(ConfirmDraftOrderInteraction)
    delete_draft_order_interactor = provide(DeleteDraftOrderInteraction)
    cancel_order_interactor = provide(CancelOrderInteraction)
    update_order_status_interactor = provide(UpdateStatusInteraction)
    process_order_interactor = provide(ProcessOrderInteraction)

    # CITY
    get_create_city_interactor = provide(CreateCityInteraction)
    
    # VEHICLES
    create_vehicle_interactor = provide(CreateVehicleInteraction)
    get_vehicle_interactor = provide(GetVehicleInteraction)
    get_vehicles_interactor = provide(GetVehiclesInteraction)
