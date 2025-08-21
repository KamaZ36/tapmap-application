from .base import Settings
from .database import DatabaseSettings
from .auth import AuthSettings
from .external import ExternalSettings
from .messaging import MessagingSettings


class AppSettings(Settings, DatabaseSettings, AuthSettings, ExternalSettings, MessagingSettings):
    """Main application settings combining all configuration sections"""
    pass


settings = AppSettings()
