from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.utils import get_datetime_utc_now


class BaseModel(DeclarativeBase):
    pass


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=get_datetime_utc_now, server_default=func.now()
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=get_datetime_utc_now,
        onupdate=get_datetime_utc_now,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
