from uuid import UUID

from sqlalchemy import select, update
from app.application.exceptions.user import UserNotFound
from app.domain.entities.user import User
from app.infrastructure.database.models.user import UserModel
from app.infrastructure.repositories.user.base import BaseUserRepository
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyUserRepository(BaseUserRepository): 
    
    def __init__(self, session: AsyncSession) -> None: 
        self.session = session    
    
    async def create(self, user: User) -> None: 
        user_model: UserModel = UserModel(
            id=user.id,
            name=user.name, 
            phone_number=user.phone_number.value,
            completed_orders_count=user.completed_orders_count,
            cancelled_orders_count=user.cancelled_orders_count,
            roles=[role.value for role in user.roles],
            base_city_id=user.base_city_id
        )
        self.session.add(user_model)
        
    async def get_by_id(self, user_id: UUID) -> User| None: 
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        user_model: UserModel | None = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None
    
    async def get_by_phone(self, phone_number: str) -> User: 
        query = select(UserModel).where(UserModel.phone_number == phone_number)
        result = await self.session.execute(query)
        user_model: UserModel | None = result.scalar_one_or_none()
        if user_model is None:
            raise UserNotFound()
        return user_model.to_entity()
    
    async def update(self, user: User) -> None: 
        stmt = (
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                name=user.name,
                phone_number=user.phone_number.value, 
                completed_orders_count=user.completed_orders_count,
                cancelled_orders_count=user.cancelled_orders_count,
                roles=[role.value for role in user.roles],
                base_city_id=user.base_city_id,
            )
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(stmt)        
        