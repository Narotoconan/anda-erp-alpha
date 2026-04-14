from app.core.database import db_disconnect
from app.core.cache import close_cache


async def shutdown():
    await db_disconnect()
    await close_cache()


__all__ = ['shutdown']
