from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
    AsyncEngine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from asyncio import current_task
from typing import Optional
from app.core.log import log

class AsyncPgSql:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.__DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

        self.__engine: Optional[AsyncEngine] = None
        self.AsyncSessionLocal: Optional[AsyncSession] = None
        self.Base = declarative_base()

        self.__create_engine()

    def __create_engine(self) -> None:
        try:

            self.__engine = create_async_engine(
                self.__DATABASE_URL,
                pool_size=5,  # 连接池大小
                max_overflow=10,  # 超过连接池大小外最多创建的连接
                pool_pre_ping=True,  # 在每次从连接池中获取连接时先发送一个简单的查询
                pool_recycle=300,  # 设置连接的最大空闲时间为 300 秒
                pool_timeout=30,  # 设置从连接池获取连接的超时时间为 30 秒
                echo_pool=True,  # 调试连接池行为
                connect_args={
                    "command_timeout": 60,  # 连接超时时间
                    "timeout": 30,  # 操作超时时间（秒）
                }
            )
        except SQLAlchemyError as e:
            log.error(f"数据库引擎创建失败！")
            raise e

    def create_session(self) -> async_scoped_session[AsyncSession]:
        try:
            _async_session = async_sessionmaker(
                bind=self.__engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=True,
                autocommit=False
            )
            return async_scoped_session(
                session_factory=_async_session,
                scopefunc=current_task
            )
        except SQLAlchemyError as e:
            log.error(f"数据库会话创建失败！")
            raise e


    async def disconnect(self) -> None:
        if self.__engine:
            await self.__engine.dispose()


__all__ = ['AsyncPgSql']
