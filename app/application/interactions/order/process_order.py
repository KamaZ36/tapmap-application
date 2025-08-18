from dataclasses import dataclass
from uuid import UUID
from loguru import logger

from app.domain.entities.order import OrderStatus

from app.config import settings

from app.infrastructure.database.transaction_manager.base import TransactionManager
from app.infrastructure.repositories.driver.base import BaseDriverRepository
from app.infrastructure.repositories.order.base import BaseOrderRepository

from app.services.geolocation import GeolocationService
from app.services.message_broker.base import BaseMessageBroker


@dataclass
class ProcessOrderInteraction:
    order_repository: BaseOrderRepository
    driver_repsoitory: BaseDriverRepository
    geolocation_service: GeolocationService
    message_broker: BaseMessageBroker
    transaction_manager: TransactionManager
        
    async def __call__(self, order_id: UUID) -> bool:
        logger.info(f"Обработка заказа {order_id}")
            
        order = await self.order_repository.get_by_id(order_id)
        
        if order.status != OrderStatus.driver_search:
            return False
        
        driver = await self.driver_repsoitory.get_nearest_free(order.points[0].coordinates)
        if not driver:
            logger.warning(f"Для заказа {order_id} не найден водитель")
            return False
        if driver.on_order:
            return False
        
        assert driver.last_location 
        submission_route = await self.geolocation_service.get_route_details(
            [
                driver.last_location,
                order.points[0].coordinates
            ]
        )
        
        order.assign_driver(
            driver_id=driver.id, 
            feeding_distance=submission_route.travel_distance, 
            feeding_time=submission_route.travel_time
        )
        driver.assign_to_order()
        
        await self.order_repository.update(order)
        await self.driver_repsoitory.update(driver)
        
        await self.transaction_manager.commit()
        
        event = {
            'order_id': str(order_id),
            'customer_id': str(order.customer_id),
            'driver_id': str(order.driver_id)
        }
            
        await self.message_broker.publish(topic=settings.driver_assigned_order_topic,key=str(order_id), value=event)
        
        logger.success(f"Заказ {order.id} успешно обработан и на него назначен водитель: {order.driver_id}")
        
        return True
    