from pydantic_settings import BaseSettings


class TgBotsSettings(BaseSettings):
    user_tg_bot_token: str

    driver_tg_bot_token: str
