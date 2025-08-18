from enum import Enum


class DriverStatus(str, Enum):
    active = 'active'
    inactive = 'inactive'
    banned = 'banned'
    