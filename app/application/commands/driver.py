from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand


@dataclass(frozen=True)
class CreateDriverCommand(BaseCommand):
    user_id: UUID
    first_name: str
    last_name: str
    middle_name: str
    license_number: str
    phone_number: str
