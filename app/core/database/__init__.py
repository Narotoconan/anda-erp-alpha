from .postgresql import AsyncPgSql
from config.settings import get_settings

settings = get_settings()

_pgsql = AsyncPgSql(
    host=settings.database.DB_HOST,
    port=settings.database.DB_PORT,
    user=settings.database.DB_USER,
    password=settings.database.DB_PASSWORD,
    database=settings.database.DB_DATABASE
)

AsyncSessionLocal = _pgsql.create_session()
Base = _pgsql.get_declarative_base()


def db_first_connection():
    from app.core.log import log

    log.info("Database first connection")
    pass


__all__ = [
    "AsyncSessionLocal",
    "Base",
    "db_first_connection",
]
