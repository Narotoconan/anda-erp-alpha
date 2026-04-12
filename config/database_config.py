from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        enable_decoding='utf-8'
    )
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = '123456'
    DB_DATABASE: str = 'postgres'


__all__ = ['DatabaseSettings']
