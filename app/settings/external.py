from pydantic_settings import BaseSettings


class ExternalSettings(BaseSettings):
    geocoder_base__url: str
    geocoder_api_key: str
    
    router_base_url: str
    
    kafka_host: str
    kafka_port: str
    
    @property
    def kafka_url(self) -> str:
        return f"{self.kafka_host}:{self.kafka_port}"
