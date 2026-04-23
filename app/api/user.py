import io
from typing import Annotated

from faker import Faker
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.core.cache import RedisPrefixes, get_redis_manager
from app.exceptions import BizException, ErrorCode, NotFoundException
from app.schemas.response import PageResponseSchema, ResponseSchema
from app.schemas.user_schema import UserSearch

router_user = APIRouter(prefix="/user", tags=["用户管理"])
fake = Faker("zh_CN")


@router_user.get("/list", summary="用户列表(分页)")
async def get_user_list_api(
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=10, ge=1, le=100, description="每页条数"),
):
    """分页查询用户列表 — 演示分页响应"""
    # 模拟数据
    total = 56
    datas = [{"name": fake.name(), "email": fake.email()} for _ in range(page_size)]

    return PageResponseSchema.ok(data=datas, total=total, page=page, page_size=page_size)


@router_user.get("/detail", summary="用户详情")
async def get_user_detail_api(user_id: int = Query(..., description="用户ID")):
    """查询单个用户 — 演示普通成功响应 & NotFoundException"""
    if user_id <= 0:
        raise NotFoundException(message=f"用户 {user_id} 不存在")

    redis_manager = get_redis_manager()
    data = {"id": user_id, "name": fake.name(), "email": fake.email()}
    await redis_manager.hset(f"{RedisPrefixes.USER_PROFILE}:{data.get('name')}", data, ex=120)
    return ResponseSchema.ok(data=data)


@router_user.get("/export", summary="导出用户(二进制文件)")
async def export_user_api():
    """
    导出用户数据为 CSV — 演示二进制文件返回

    注意: 文件下载场景直接返回 StreamingResponse / FileResponse,
    不经过统一 JSON 响应格式包装。
    """
    # 模拟生成 CSV
    buffer = io.StringIO()
    buffer.write("id,name,email\n")
    for i in range(1, 11):
        buffer.write(f"{i},{fake.name()},{fake.email()}\n")

    content = buffer.getvalue().encode("utf-8-sig")  # BOM 头兼容 Excel
    return StreamingResponse(
        io.BytesIO(content),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=users.csv"},
    )


@router_user.get("/error-demo", summary="异常演示")
async def error_demo_api(error_type: str = Query(default="biz", description="biz / auth / internal")):
    """手动触发不同类型异常 — 仅供开发调试"""
    if error_type == "biz":
        raise BizException(ErrorCode.FAIL, message="这是一个业务异常示例")
    elif error_type == "auth":
        from app.exceptions import AuthException

        raise AuthException(message="请先登录")
    elif error_type == "internal":
        # 触发未处理异常，走兜底 handler
        raise RuntimeError("模拟系统内部错误")
    return ResponseSchema.ok(message="没有触发异常")


@router_user.get("/search", summary="用户搜索")
async def search_user(params: Annotated[UserSearch, Query()]):
    return ResponseSchema.ok(data=params.model_dump())


__all__ = ["router_user"]
