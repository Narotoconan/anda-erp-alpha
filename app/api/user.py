from fastapi import APIRouter
from app.core.cache import get_redis_manager, RedisPrefixes
from faker import Faker

router_user = APIRouter(prefix="/user", tags=["用户管理"])
fake = Faker('zh_CN')

@router_user.get("/list", summary="用户列表")
async def get_user_api(params):
    redis_manager = get_redis_manager()

    data = {"name": fake.name(), "email": fake.email()}
    await redis_manager.hset(f"{RedisPrefixes.USER_PROFILE}:{data.get('name')}", data, ex=120)
    return data


__all__ = ["router_user"]
