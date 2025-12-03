from app.core.config.tg_bots import TgBotsSettings
from .base import Settings
from .database import DatabaseSettings
from .auth import AuthSettings
from .external import ExternalSettings
from .messaging import MessagingSettings


class AppSettings(
    Settings,
    DatabaseSettings,
    AuthSettings,
    ExternalSettings,
    MessagingSettings,
    TgBotsSettings,
):
    """Main application settings combining all configuration sections"""

    pass


settings = AppSettings()
