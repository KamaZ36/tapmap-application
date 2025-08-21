from pydantic_settings import BaseSettings


class MessagingSettings(BaseSettings):
    order_status_update_topic: str
    driver_assigned_order_topic: str
