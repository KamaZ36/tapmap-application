from dataclasses import dataclass
from uuid import UUID


class DriverApplication:
    id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    phone_number: str
    driver_license_number: str
    is_verified: bool = False

    def confirm(self) -> None:
        self.is_verified = True
