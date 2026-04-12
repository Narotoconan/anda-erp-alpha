from fastapi import FastAPI
from config.settings import get_settings
from app.core.events import lifespan
from app.core.log import register_log
from app.api import register_router

settings = get_settings()

app = FastAPI(
    title=settings.app.APP_NAME,
    version=settings.app.APP_VERSION,
    lifespan=lifespan
)

# 注册日志
register_log()

# 注册路由
register_router(app)
