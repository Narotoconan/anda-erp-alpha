from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache
from .app_config import AppSettings
from .database_config import DatabaseSettings
from  .logger_config import LoggerSettings



class Settings(BaseSettings):

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    logger: LoggerSettings = Field(default_factory=LoggerSettings)

@lru_cache
def get_settings() -> Settings:
    return Settings()

__all__ = ['get_settings']