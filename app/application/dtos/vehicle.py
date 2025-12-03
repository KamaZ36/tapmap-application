from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=False)
class VehicleForOrderDTO:
    id: UUID
    brand: str
    model: str
    color: str
    number: str
