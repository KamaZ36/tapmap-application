from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase): 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=func.now())
