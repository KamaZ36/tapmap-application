from app.application.dtos.driver import DriverDTO
from app.infrastructure.database.models.driver import DriverModel


def convert_driver_model_to_dto(driver: DriverModel) -> DriverDTO:
    return DriverDTO(
        id=driver.id,
        first_name=driver.first_name,
        last_name=driver.last_name,
        middle_name=driver.middle_name,
        phone_number=driver.phone_number,
        license_number=driver.license_number,
        completed_orders_count=driver.completed_orders_count,
        cancelled_orders_count=driver.cancelled_orders_count,
        status=driver.status,
        on_order=driver.on_order,
        on_shift=driver.on_shift,
        created_at=driver.created_at,
    )
