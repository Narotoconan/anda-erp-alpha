from pydantic_settings import BaseSettings
from functools import lru_cache
import tomllib
import os


@lru_cache(maxsize=1)
def load_pyproject_toml():
    with open('pyproject.toml', 'rb') as config_file:
        return tomllib.load(config_file)


class AppSettings(BaseSettings):
    pyproject: dict = load_pyproject_toml()

    APP_NAME: str = pyproject.get("project").get("name")
    APP_VERSION: str = pyproject.get("project").get("version")
    BASE_PATH: str = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))


__all__ = ['AppSettings']
