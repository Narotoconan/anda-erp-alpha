from .postgresql import AsyncPgSql
from config import DATABASE_SETTINGS

_pgsql = AsyncPgSql(
    host=DATABASE_SETTINGS.DB_HOST,
    port=DATABASE_SETTINGS.DB_PORT,
    user=DATABASE_SETTINGS.DB_USER,
    password=DATABASE_SETTINGS.DB_PASSWORD,
    database=DATABASE_SETTINGS.DB_DATABASE,
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
