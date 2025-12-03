from enum import Enum


class UserStatus(str, Enum):
    active = "active"
    blocked = "blocked"


class UserRole(str, Enum):
    user = "user"
    driver = "driver"
    admin = "admin"
