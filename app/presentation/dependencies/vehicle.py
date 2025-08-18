from dishka import Provider, Scope, provide

from app.application.interactions.vehicle.create_vehicle import CreateVehicleInteraction
from app.application.interactions.vehicle.get_vehicle import GetVehicleInteraction
from app.application.interactions.vehicle.get_vehicles import GetVehiclesInteraction
from app.infrastructure.unit_of_work.base import BaseUnitOfWork

class VehicleInteractions(Provider):
    create_vehicle_interactor = provide(CreateVehicleInteraction, scope=Scope.REQUEST)
    
    get_vehicle_interactor = provide(GetVehicleInteraction, scope=Scope.REQUEST)
    get_vehicles_interactor = provide(GetVehiclesInteraction, scope=Scope.REQUEST)
    