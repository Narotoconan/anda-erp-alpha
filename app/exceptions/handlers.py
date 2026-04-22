"""
全局异常处理器

注册到 FastAPI app 后，所有异常会被统一拦截并转换为标准 JSON 响应格式。
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.log import log

from app.exceptions.errors import BizException, ErrorCode


def _build_error_response(
    *,
    http_status: int,
    code: int,
    message: str,
    result: dict | None = None,
) -> JSONResponse:
    """构建统一错误 JSON 响应"""
    return JSONResponse(
        status_code=http_status,
        content={
            "code": code,
            "message": message,
            "result": result or {},
        },
    )


# ==================== 异常处理函数 ====================


async def biz_exception_handler(_request: Request, exc: BizException) -> JSONResponse:
    """业务异常处理"""
    log.warning(
        "BizException | code={} message={} path={}",
        exc.code,
        exc.message,
        _request.url.path,
    )
    return _build_error_response(
        http_status=exc.http_status,
        code=exc.code,
        message=exc.message,
        result=exc.result,
    )


async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Pydantic / FastAPI 参数校验异常处理
    将原始 errors 信息格式化后放入 message, 方便前端展示
    """
    errors = exc.errors()
    # 取第一条错误的简明描述作为 message
    first = errors[0] if errors else {}
    loc = " -> ".join(str(l) for l in first.get("loc", []))
    msg = first.get("msg", "参数校验失败")
    detail = f"{loc}: {msg}" if loc else msg

    log.warning(
        "ValidationError | path={} detail={}",
        _request.url.path,
        detail,
    )
    return _build_error_response(
        http_status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        code=ErrorCode.PARAMS_INVALID,
        message=detail,
        result={"errors": errors},
    )


async def http_exception_handler(
    _request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """
    Starlette / FastAPI HTTPException 处理
    将框架原生的 HTTP 异常也转换为统一格式
    """
    # 映射常见 HTTP 状态码到业务错误码
    _STATUS_CODE_MAP: dict[int, int] = {
        401: ErrorCode.UNAUTHORIZED,
        403: ErrorCode.FORBIDDEN,
        404: ErrorCode.NOT_FOUND,
        405: ErrorCode.PARAMS_INVALID,
        422: ErrorCode.PARAMS_INVALID,
        429: ErrorCode.FAIL,
    }
    code = _STATUS_CODE_MAP.get(exc.status_code, ErrorCode.FAIL)

    log.warning(
        "HTTPException | status={} detail={} path={}",
        exc.status_code,
        exc.detail,
        _request.url.path,
    )
    return _build_error_response(
        http_status=exc.status_code,
        code=code,
        message=str(exc.detail) if exc.detail else "请求失败",
    )


async def unhandled_exception_handler(
    _request: Request, exc: Exception
) -> JSONResponse:
    """
    兜底: 未被捕获的异常
    生产环境隐藏堆栈，仅记录日志
    """
    log.exception(
        "UnhandledException | path={} error={}",
        _request.url.path,
        str(exc),
    )
    return _build_error_response(
        http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code=ErrorCode.INTERNAL_ERROR,
        message="系统内部错误，请稍后重试",
    )


# ==================== 注册入口 ====================


def register_exception_handlers(app: FastAPI) -> None:
    """一键注册所有异常处理器"""
    app.add_exception_handler(BizException, biz_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)


__all__ = ["register_exception_handlers"]

