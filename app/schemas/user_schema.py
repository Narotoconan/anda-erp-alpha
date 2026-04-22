from .base_schema import BaseSchema
from pydantic import Field


class UserSearch(BaseSchema):
    username: str = Field(..., min_length=3, max_length=10, description="用户名称")
    gender: int = Field(..., ge=0, le=1, description="性别")


__all__ = [
    "UserSearch",
]
