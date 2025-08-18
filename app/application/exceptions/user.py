from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions.base import LogicException


@dataclass
class UserNotFound(LogicException):
    
    @property
    def message(self) -> str:
        return "Пользователь не найден"

@dataclass
class NotSetBaseCityForUser(LogicException):
    user_id: UUID
    
    @property
    def message(self) -> str:
        return f"У пользователя {str(self.user_id)} не установлен город по умолчанию"
