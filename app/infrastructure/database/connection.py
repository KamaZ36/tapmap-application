from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

from app.core.config import settings


engine: AsyncEngine = create_async_engine(
    settings.db_url, echo=settings.debug, future=True, plugins=["geoalchemy2"]
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
