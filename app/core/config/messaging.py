from pydantic_settings import BaseSettings


class MessagingSettings(BaseSettings):
    order_confirmed_topic: str
    order_status_update_topic: str
    driver_assigned_order_topic: str
    order_cancel_topic: str
