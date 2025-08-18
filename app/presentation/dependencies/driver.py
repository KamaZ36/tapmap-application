from dishka import Provider, Scope, provide

from app.application.interactions.driver.create_driver import CreateDriverInteraction
from app.application.interactions.driver.get_active_order import GetActiveOrderForDriverInteraction
from app.application.interactions.driver.get_driver import GetDriverInteraction
from app.application.interactions.driver.get_last_location import GetLastLocationDriverInteraction
from app.application.interactions.driver.switch_on_shift import SwitchDriverOnShiftInteraction
from app.application.interactions.driver.update_location import UpdateLocationInteraction


class DriverInteractions(Provider):
    scope = Scope.REQUEST
    
    # Driver management
    get_driver_interactor = provide(GetDriverInteraction)
    create_driver_interactor = provide(CreateDriverInteraction)
    
    # Location related
    update_location_interactor = provide(UpdateLocationInteraction)
    get_location_interactor = provide(GetLastLocationDriverInteraction)
    
    # Shift and orders
    switch_on_shift_interactor = provide(SwitchDriverOnShiftInteraction)
    get_active_order_interactor = provide(GetActiveOrderForDriverInteraction)
