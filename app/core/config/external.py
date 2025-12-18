from pydantic_settings import BaseSettings


class ExternalSettings(BaseSettings):
    geocoder_base__url: str
    geocoder_api_key: str

    router_base_url: str
