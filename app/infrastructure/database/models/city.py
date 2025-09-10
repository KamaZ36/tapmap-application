from decimal import Decimal
from uuid import UUID

from geoalchemy2 import Geometry, WKBElement, WKTElement
from geoalchemy2.shape import to_shape

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import DECIMAL

from app.domain.entities.city import City

from app.infrastructure.database.models.base import BaseModel


class CityModel(BaseModel):
    __tablename__ = "cities"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, unique=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column(nullable=False)

    base_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    price_per_kilometer: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    service_commission_pct: Mapped[Decimal] = mapped_column(
        DECIMAL(5, 2), nullable=False
    )

    polygon: Mapped[WKBElement] = mapped_column(
        Geometry("POLYGON", srid=4326), nullable=False
    )

    @classmethod
    def from_entity(cls, city: City) -> "CityModel":
        polygon_wkt = WKTElement(city.polygon.wkt, srid=4326)
        return cls(
            id=city.id,
            name=city.name,
            state=city.state,
            base_price=city.base_price,
            price_per_kilometer=city.price_per_kilometer,
            service_commission_pct=city.service_commission_pct,
            polygon=polygon_wkt,
        )

    def to_entity(self) -> City:
        # wkb_data = bytes(self.polygon.data)
        polygon = to_shape(self.polygon)
        # polygon = from_wkb(wkb_data)
        return City(
            id=self.id,
            name=self.name,
            state=self.state,
            base_price=Decimal(self.base_price),
            price_per_kilometer=Decimal(self.price_per_kilometer),
            service_commission_pct=Decimal(self.service_commission_pct),
            polygon=polygon,  # type: ignore
        )
