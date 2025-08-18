from typing import Type
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.application.exceptions.user import UserNotFound
from app.domain.exceptions.base import AppException
from app.services.exceptions.auth import InvalidAccessToken

def get_http_status_code(exc: Exception) -> int:
    """Маппинг исключений на HTTP статус коды"""
    exc_to_status: dict[Type[Exception], int] = {
        InvalidAccessToken: status.HTTP_401_UNAUTHORIZED,
        UserNotFound: status.HTTP_404_NOT_FOUND
    }
    return exc_to_status.get(type(exc), status.HTTP_400_BAD_REQUEST)

async def generate_exception_request(request: Request, exc: AppException) -> JSONResponse:
    status_code = get_http_status_code(exc)
    
    return JSONResponse(
        status_code=status_code,
        content={
            "message": exc.message
        }
    )
