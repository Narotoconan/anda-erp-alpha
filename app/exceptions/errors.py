"""
业务错误码枚举 & 自定义异常

错误码规范:
    0       : 成功
    -1      : 通用失败
    1xxx    : 认证/授权相关
    2xxx    : 参数校验相关
    3xxx    : 资源相关
    4xxx    : 第三方服务相关
    5xxx    : 系统内部错误
"""

from enum import IntEnum


class ErrorCode(IntEnum):
    """业务错误码"""

    # 通用
    SUCCESS = 0
    FAIL = -1

    # 认证/授权 1xxx
    UNAUTHORIZED = 1001
    TOKEN_EXPIRED = 1002
    TOKEN_INVALID = 1003
    FORBIDDEN = 1004

    # 参数校验 2xxx
    PARAMS_INVALID = 2001
    PARAMS_MISSING = 2002

    # 资源 3xxx
    NOT_FOUND = 3001
    ALREADY_EXISTS = 3002
    RESOURCE_GONE = 3003

    # 第三方服务 4xxx
    THIRD_PARTY_ERROR = 4001
    THIRD_PARTY_TIMEOUT = 4002

    # 系统 5xxx
    INTERNAL_ERROR = 5001
    DATABASE_ERROR = 5002
    CACHE_ERROR = 5003


# 错误码 -> 默认消息映射
_ERROR_MESSAGES: dict[int, str] = {
    ErrorCode.SUCCESS: "success",
    ErrorCode.FAIL: "操作失败",
    ErrorCode.UNAUTHORIZED: "未登录或登录已过期",
    ErrorCode.TOKEN_EXPIRED: "Token 已过期",
    ErrorCode.TOKEN_INVALID: "Token 无效",
    ErrorCode.FORBIDDEN: "权限不足",
    ErrorCode.PARAMS_INVALID: "参数校验失败",
    ErrorCode.PARAMS_MISSING: "缺少必要参数",
    ErrorCode.NOT_FOUND: "资源不存在",
    ErrorCode.ALREADY_EXISTS: "资源已存在",
    ErrorCode.RESOURCE_GONE: "资源已被删除",
    ErrorCode.THIRD_PARTY_ERROR: "第三方服务异常",
    ErrorCode.THIRD_PARTY_TIMEOUT: "第三方服务超时",
    ErrorCode.INTERNAL_ERROR: "系统内部错误",
    ErrorCode.DATABASE_ERROR: "数据库异常",
    ErrorCode.CACHE_ERROR: "缓存服务异常",
}


def get_error_message(code: int) -> str:
    """根据错误码获取默认消息"""
    return _ERROR_MESSAGES.get(code, "未知错误")


class BizException(Exception):
    """
    业务异常基类

    用法:
        raise BizException(ErrorCode.NOT_FOUND)
        raise BizException(ErrorCode.PARAMS_INVALID, message="邮箱格式不正确")
        raise BizException(ErrorCode.FAIL, message="自定义错误", http_status=400)
    """

    def __init__(
        self,
        code: int | ErrorCode = ErrorCode.FAIL,
        *,
        message: str | None = None,
        http_status: int = 200,
        result: dict | None = None,
    ):
        self.code = int(code)
        self.message = message or get_error_message(self.code)
        self.http_status = http_status
        self.result = result or {}
        super().__init__(self.message)


class AuthException(BizException):
    """认证/授权异常"""

    def __init__(
        self,
        code: int | ErrorCode = ErrorCode.UNAUTHORIZED,
        *,
        message: str | None = None,
    ):
        super().__init__(code, message=message, http_status=401)


class ForbiddenException(BizException):
    """权限不足异常"""

    def __init__(self, *, message: str | None = None):
        super().__init__(ErrorCode.FORBIDDEN, message=message, http_status=403)


class NotFoundException(BizException):
    """资源不存在异常"""

    def __init__(self, *, message: str | None = None):
        super().__init__(ErrorCode.NOT_FOUND, message=message, http_status=404)


class ParamsException(BizException):
    """参数校验异常"""

    def __init__(self, *, message: str | None = None):
        super().__init__(ErrorCode.PARAMS_INVALID, message=message, http_status=422)


__all__ = [
    "ErrorCode",
    "get_error_message",
    "BizException",
    "AuthException",
    "ForbiddenException",
    "NotFoundException",
    "ParamsException",
]

