from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import tomllib
import os


@lru_cache(maxsize=1)
def load_pyproject_toml():
    with open('pyproject.toml', 'rb') as config_file:
        _config = tomllib.load(config_file)
    return _config.get('project').get('name'), _config.get('project').get('version')

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        enable_decoding='utf-8'
    )
    _name, _version = load_pyproject_toml()

    APP_NAME: str = _name
    APP_VERSION: str = _version
    BASE_PATH: str = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))


__all__ = ['AppSettings']
