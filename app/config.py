from pydantic_settings import BaseSettings

class Settings(BaseSettings): 
    app_name: str 
    debug: bool 
    
    geocoder_base__url: str 
    geocoder_api_key: str

    router_base_url: str 
    
    
    access_jwt_secret_key: str 
    refresh_jwt_secret_key: str
    algorithm: str 
    accesss_token_expire_hours: int 
    refresh_token_expire_days: int 
    
    db_user: str 
    db_password: str 
    db_host: str 
    db_port: str 
    db_database: str 

    redis_host: str 
    redis_port: str 
    
    kafka_host: str 
    kafka_port: str
        
    order_status_update_topic: str
    driver_assigned_order_topic: str 

    @property
    def kafka_url(self) -> str:
        return f"{self.kafka_host}:{self.kafka_port}"

    @property
    def redis_url(self) -> str: 
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_database}"

    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"


settings = Settings()
