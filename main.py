from fastapi import FastAPI
from config import APP_SETTINGS
from app.core.events import lifespan
from app.core.log import register_log
from app.api import register_router

app = FastAPI(
    title=APP_SETTINGS.APP_NAME,
    version=APP_SETTINGS.APP_VERSION,
    lifespan=lifespan
)

# 注册日志
register_log()

# 注册路由
register_router(app)
