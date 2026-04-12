from .postgresql import AsyncPgSql
from config.settings import get_settings
from app.core.log import log


settings = get_settings()

_pgsql = AsyncPgSql(
    host=settings.database.DB_HOST,
    port=settings.database.DB_PORT,
    user=settings.database.DB_USER,
    password=settings.database.DB_PASSWORD,
    database=settings.database.DB_DATABASE
)

AsyncSessionLocal = _pgsql.AsyncSessionLocal
Base = _pgsql.Base


def db_first_connection():
    log.info("Database first connection")


async def db_disconnect():
    await _pgsql.disconnect()
    log.info("数据库连接已关闭！")


__all__ = [
    "AsyncSessionLocal",
    "Base",
    "db_first_connection",
    "db_disconnect"
]
