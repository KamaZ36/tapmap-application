from dishka import Provider, provide, Scope

from app.application.queries.driver.get_by_id import GetDriverByIdQueryHandler
from app.application.queries.order.get_active_for_customer import (
    GetActiveOrderForCustomerQueryHandler,
)
from app.application.queries.order.get_active_for_driver import (
    GetActiveOrderForDriverQueryHandler,
)
from app.application.queries.order.get_order_by_id import GetOrderByIdQueryHandler
from app.application.queries.order.get_orders import GetOrdersListQueryHandler
from app.application.queries.user.get_by_id import GetUserByIdQueryHandler
from app.application.queries.user.get_by_phone_number import GetUserByPhoneQueryHandler


class QueryHandlersProvider(Provider):
    scope = Scope.REQUEST

    # USER
    get_user_by_id_query_handler = provide(GetUserByIdQueryHandler)
    get_user_by_phone_query_handler = provide(GetUserByPhoneQueryHandler)

    # DRIVER
    get_driver_by_id_query_handler = provide(GetDriverByIdQueryHandler)

    # ORDER
    get_order_by_id_query_handler = provide(GetOrderByIdQueryHandler)
    get_orders_list_query_handler = provide(GetOrdersListQueryHandler)
    get_active_order_for_user_query_handler = provide(
        GetActiveOrderForCustomerQueryHandler
    )
    get_active_order_for_driver_query_handler = provide(
        GetActiveOrderForDriverQueryHandler
    )
