from dataclasses import dataclass
import re

from app.domain.exceptions.phone_number import InvalidPhoneNumber
from app.domain.value_objects.base import ValueObject


@dataclass(frozen=True)
class PhoneNumber(ValueObject):
    value: str

    def __post_init__(self):
        cleaned = re.sub(r"[^\d]", "", self.value)

        if cleaned.startswith("8"):
            cleaned = "7" + cleaned[1:]
        elif cleaned.startswith("+7"):
            cleaned = "7" + cleaned[2:]
        elif cleaned.startswith("7"):
            pass
        else:
            raise InvalidPhoneNumber(phone_number=self.value)

        if not re.fullmatch(r"7\d{10}", cleaned):
            raise InvalidPhoneNumber(phone_number=self.value)

        # Обновляем значение (только через object.__setattr__ из-за frozen=True)
        object.__setattr__(self, "value", cleaned)

    def __str__(self) -> str:
        return self.value
