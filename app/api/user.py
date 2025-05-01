from fastapi import APIRouter

router_user = APIRouter(prefix="/user", tags=["用户管理"])


@router_user.get("/list", summary="用户列表")
async def get_user_api(params):
    return params


__all__ = ["router_user"]
