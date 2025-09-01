from datetime import datetime, timezone
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def get_datetime_utc_now() -> datetime:
    datetime_now = datetime.now(tz=timezone.utc)
    return datetime_now.replace(tzinfo=None)


class BaseModel(DeclarativeBase): 
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=get_datetime_utc_now, 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=get_datetime_utc_now,
        onupdate=get_datetime_utc_now,
        server_default=func.now(),
        server_onupdate=func.now()
    )
