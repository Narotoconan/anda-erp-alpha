from app.core.database import db_disconnect


async def shutdown():
    await db_disconnect()


__all__ = ['shutdown']
