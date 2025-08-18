from uuid import UUID

from geoalchemy2 import Geometry, WKBElement
from geoalchemy2.shape import to_shape

from shapely import Point as SH_Point

from app.domain.entities.driver import Driver, DriverStatus
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.database.models.base import BaseModel

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.dialects.postgresql import ENUM


class DriverModel(BaseModel): 
    __tablename__ = "drivers"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, unique=True)

    first_name: Mapped[str] = mapped_column(unique=False)
    last_name: Mapped[str] = mapped_column(unique=False)
    middle_name: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(unique=True)

    license_number: Mapped[str] = mapped_column(unique=True, nullable=False)

    completed_orders_count: Mapped[int] = mapped_column(server_default='0', default=0)
    cancelled_orders_count: Mapped[int] = mapped_column(server_default='0', default=0)
    
    status: Mapped[DriverStatus] = mapped_column(ENUM(DriverStatus), nullable=False, server_default=DriverStatus.active.value, default=DriverStatus.active)
    
    last_location: Mapped[WKBElement] = mapped_column(Geometry('POINT', srid=4326), index=True, nullable=True)
    
    on_order: Mapped[bool] = mapped_column(server_default="False", default=False)
    on_shift: Mapped[bool] = mapped_column(server_default='False', default=False)
    
    vehicles: Mapped[list["VehicleModel"]] = relationship(back_populates='driver')
    
    def to_entity(self) -> Driver: 
        coordinates = None
        if self.last_location:
            sh_point = to_shape(self.last_location)
            if isinstance(sh_point, SH_Point):
                coordinates = Coordinates(
                    latitude=sh_point.y,
                    longitude=sh_point.x
                )
        return Driver(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            license_number=self.license_number,
            phone_number=PhoneNumber(self.phone_number), # type: ignore
            completed_orders_count=self.completed_orders_count,
            cancelled_orders_count=self.cancelled_orders_count,
            status=self.status,
            last_location=coordinates,
            on_order=self.on_order,
            on_shift=self.on_shift
        )
    