from fastapi import FastAPI

from dishka.integrations.fastapi import setup_dishka

from app.domain.exceptions.base import AppException
from app.presentation.api.v1 import (
    user_router,
    authentication_router,
    draft_order_router,
    order_router,
    city_router,
    admin_router,
    driver_router,
    vehicle_router,
)
from app.presentation.api.v1.exception_handler import generate_exception_request
from app.presentation.dependencies.container import container
from app.presentation.api.lifespan import lifespan


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    # Setup DI
    setup_dishka(container=container, app=app)

    # Setup exception handlers
    app.add_exception_handler(AppException, generate_exception_request)

    # Include routers
    app.include_router(authentication_router, prefix="/auth", tags=["Аутентификация"])
    app.include_router(user_router, prefix="/users", tags=["Пользователи"])
    app.include_router(driver_router, prefix="/drivers", tags=["Водители"])
    app.include_router(
        draft_order_router, prefix="/orders/draft", tags=["Черновики заказов"]
    )
    app.include_router(order_router, prefix="/orders", tags=["Заказы"])
    app.include_router(
        vehicle_router, prefix="/vehicles", tags=["Транспортные средства"]
    )
    app.include_router(city_router, prefix="/cities", tags=["Города"])
    app.include_router(admin_router, prefix="/admin", tags=["Администратор"])

    return app
