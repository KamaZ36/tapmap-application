from dataclasses import dataclass, field
from uuid import UUID

from app.domain.entities.base import Entity
from app.domain.enums.user_role import UserRole
from app.domain.value_objects.phone_number import PhoneNumber
     

@dataclass(kw_only=True)
class User(Entity): 
    name: str 
    phone_number: PhoneNumber
    
    completed_orders_count: int = 0
    cancelled_orders_count: int = 0

    roles: list[UserRole] = field(default_factory=lambda: [UserRole.user])

    base_city_id: UUID | None = None

    def complete_order(self) -> None: 
        self.completed_orders_count += 1
        
    def cancel_order(self) -> None: 
        self.cancelled_orders_count += 1

    def set_base_city(self, city_id: UUID) -> None: 
        self.base_city_id = city_id
        
    def add_role(self, role: UserRole) -> None:
        if role in self.roles:
            return
        self.roles.append(role)

    def has_role(self, role: UserRole) -> bool:
        return role in self.roles
    
    def remove_role(self, role: UserRole) -> None:
        if role in self.roles:
            self.roles.remove(role)
