from dataclasses import dataclass
import re
from typing import ClassVar

from app.domain.value_objects.base import ValueObject

@dataclass(frozen=True)
class VehicleNumber(ValueObject): 
    value: str
    
    _pattern: ClassVar[re.Pattern] = re.compile(r"^[АВЕКМНОРСТУХ]{1}\d{3}[АВЕКМНОРСТУХ]{2}\d{2,3}$", re.IGNORECASE)

    def __post_init__(self) -> None: 
        normalized = self.value.replace(" ", "").upper()
        if not self._pattern.match(normalized):
            raise ValueError(f"Некорректный номер автомобиля: {self.value}")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str: 
        return str(self.value)
        