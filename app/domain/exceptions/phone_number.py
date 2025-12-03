from dataclasses import dataclass

from app.domain.exceptions.base import AppException


@dataclass(frozen=True, eq=False)
class InvalidPhoneNumber(AppException):
    error_code = "INVALID_PHONE_NUMBER"

    phone_number: str

    @property
    def message(self) -> str:
        return f"Невалидный номер телефона: {self.phone_number} символов."
