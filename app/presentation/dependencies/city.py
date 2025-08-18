from dishka import Provider, Scope, provide

from app.application.interactions.city.create import CreateCityInteraction


class CityInteractions(Provider):
    
    get_create_city_interactor = provide(CreateCityInteraction, scope=Scope.REQUEST)
    