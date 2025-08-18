from dishka import Provider, Scope, provide

from app.application.interactions.user.create_user import CreateUserInteraction
from app.application.interactions.user.get_active_order import GetActiveOrderForUserInteraction
from app.application.interactions.user.get_user import GetUserInteractor
from app.application.interactions.user.set_base_location import SetBaseLocationUserInteraction
from app.infrastructure.unit_of_work.base import BaseUnitOfWork


class UserInteractions(Provider):
    
    # QUERY
    get_user_interactor = provide(GetUserInteractor, scope=Scope.REQUEST)
    get_active_order_for_user_interactor = provide(GetActiveOrderForUserInteraction, scope=Scope.REQUEST)
    
    # COMMANDS
    create_user_interactor = provide(CreateUserInteraction, scope=Scope.REQUEST)
    set_user_base_city_interactor = provide(SetBaseLocationUserInteraction, scope=Scope.REQUEST)
    
    