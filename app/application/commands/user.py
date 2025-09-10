from dataclasses import dataclass

from app.application.commands.base import BaseCommand


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    phone_number: str
    name: str


@dataclass(frozen=True)
class SetBaseUserLocationCommand(BaseCommand):
    coordinates: tuple[float, float]
