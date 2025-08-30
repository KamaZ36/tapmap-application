from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_database: str
    
    redis_host: str
    redis_port: str
    
    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_database}"
    
    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"
