from typing import Protocol
from uuid import UUID

from app.domain.entities.draft_order import DraftOrder


class BaseDraftOrderRepository(Protocol): 
    
    async def create(self, draft_order: DraftOrder) -> None: ...
    
    async def get_by_customer_id(self, customer_id: UUID) -> DraftOrder: ...

    async def update(self, draft_order: DraftOrder) -> None: ...
        
    async def delete(self, customer_id: UUID) -> None: ...
        