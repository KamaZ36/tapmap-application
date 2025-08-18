from dishka import make_async_container

from app.presentation.dependencies.city import CityInteractions
from app.presentation.dependencies.driver import DriverInteractions
from app.presentation.dependencies.database import DatabaseProvider
from app.presentation.dependencies.order import DraftOrdersInteractions
from app.presentation.dependencies.provider import AppProvider
from app.presentation.dependencies.user import UserInteractions
from app.presentation.dependencies.vehicle import VehicleInteractions
from app.presentation.dependencies.repositories import RepositoriesProvider


container = make_async_container(
    AppProvider(), 
    DatabaseProvider(),
    RepositoriesProvider(),
    DraftOrdersInteractions(), 
    UserInteractions(), 
    CityInteractions(), 
    DriverInteractions(),
    VehicleInteractions()
)
