from enum import Enum


class UserRole(str, Enum):
    user = 'user'
    driver = 'driver'
    admin = 'admin'
    