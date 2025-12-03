import uvicorn

from fastapi import FastAPI

from app.domain.exceptions.base import AppException

from app.api.v1.entrypoints import (
    authentication_router,
    user_router,
    order_router,
    driver_router,
    admin_router,
)
from app.api.exception_handler import generate_exception_request
from app.api.lifespan import lifespan


def include_router(app: FastAPI) -> None:
    app.include_router(authentication_router, prefix="/auth", tags=["Аутентификация"])
    app.include_router(user_router, prefix="/users", tags=["Пользователи"])
    app.include_router(driver_router, prefix="/drivers", tags=["Водители"])
    app.include_router(order_router, prefix="/orders", tags=["Заказы"])
    app.include_router(admin_router, prefix="/admin", tags=["Для администраторов"])


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    include_router(app=app)

    # Setup exception handlers
    app.add_exception_handler(AppException, generate_exception_request)

    return app


if __name__ == "__main__":
    app = create_app()

    uvicorn.run(app, host="0.0.0.0", port=8000)
