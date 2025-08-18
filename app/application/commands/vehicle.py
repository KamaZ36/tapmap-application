from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand


@dataclass(frozen=True)
class CreateVehcielCommand(BaseCommand):
    driver_id: UUID
    brand: str
    model: str
    color: str
    number: str
