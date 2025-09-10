from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import ClassVar, Union

from app.domain.value_objects.base import ValueObject


@dataclass(frozen=True)
class Money(ValueObject):
    value: Decimal

    _valid_currencies: ClassVar[set[str]] = {"RUB"}

    def __post_init__(self) -> None:
        if not isinstance(self.value, Decimal):
            try:
                value = Decimal(self.value)
                if value < 0:
                    raise ValueError("Сумма валюты не может быть отрицательной.")
            except:
                raise ValueError(f"Неверное значение суммы: {self.value}")
            object.__setattr__(self, "value", value)

        try:
            rounded = self.value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            object.__setattr__(self, "value", rounded)
        except InvalidOperation as e:
            raise ValueError(f"Неверное значение суммы: {self.value}") from e

    def __add__(self, other: Union["Money", Decimal, int, float]) -> "Money":
        if isinstance(other, Money):
            other_value = other.value
        elif isinstance(other, (Decimal, int, float)):
            other_value = Decimal(str(other))
        else:
            return NotImplemented

        result = self.value + other_value
        return Money(result)

    def __sub__(self, other: Union["Money", Decimal, int, float]) -> "Money":
        if isinstance(other, Money):
            other_value = other.value
        elif isinstance(other, (Decimal, int, float)):
            other_value = Decimal(str(other))
        else:
            return NotImplemented

        result = self.value - other_value
        if result < 0:
            raise ValueError("Результат вычитания валют не может быть отрицательным")
        return Money(result)

    def __mul__(self, other: Union[int, float, Decimal]) -> "Money":
        if not isinstance(other, (int, float, Decimal)):
            return NotImplemented

        other_value = Decimal(str(other))
        result = self.value * other_value
        return Money(result)

    def __rmul__(self, other: Union[int, float, Decimal]) -> "Money":
        # Чтобы работало с обеих сторон: 5 * money
        return self.__mul__(other)

    def __truediv__(self, other: Union[int, float, Decimal]) -> "Money":
        if not isinstance(other, (int, float, Decimal)):
            return NotImplemented

        other_value = Decimal(str(other))
        if other_value == 0:
            raise ZeroDivisionError("Деление на ноль запрещено.")

        result = self.value / other_value
        return Money(result)
