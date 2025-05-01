from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.core.log import log


async def get_db() -> AsyncSession:
    # 每个请求独立作用域
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
        AsyncSessionLocal.remove()  # 关键清理操作
