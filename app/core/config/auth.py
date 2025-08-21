from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    access_jwt_secret_key: str
    refresh_jwt_secret_key: str
    algorithm: str
    accesss_token_expire_hours: int
    refresh_token_expire_days: int
