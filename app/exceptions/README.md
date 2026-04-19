# 异常处理使用指南

## 快速上手

```python
from app.exceptions import BizException, NotFoundException, AuthException, ForbiddenException, ParamsException, ErrorCode
```

---

## 一、内置异常类型

| 异常类 | HTTP 状态码 | 业务错误码 | 适用场景 |
|---|---|---|---|
| `BizException` | 自定义(默认200) | 自定义(默认-1) | 通用业务异常基类 |
| `AuthException` | 401 | 1001 | 未登录 / Token 无效 |
| `ForbiddenException` | 403 | 1004 | 权限不足 |
| `NotFoundException` | 404 | 3001 | 资源不存在 |
| `ParamsException` | 422 | 2001 | 参数校验失败 |

---

## 二、使用示例

### 1. 资源不存在

```python
from app.exceptions import NotFoundException

async def get_user(user_id: int):
    user = await db.get(user_id)
    if not user:
        raise NotFoundException(message=f"用户 {user_id} 不存在")
    return user
```

响应：
```json
{"code": 3001, "message": "用户 99 不存在", "result": {}}
```

---

### 2. 权限校验

```python
from app.exceptions import AuthException, ForbiddenException

# 未登录
raise AuthException(message="请先登录")
# → HTTP 401, code=1001

# 无权限
raise ForbiddenException(message="仅管理员可操作")
# → HTTP 403, code=1004
```

---

### 3. 通用业务异常（自定义错误码）

```python
from app.exceptions import BizException, ErrorCode

# 使用枚举错误码（message 自动填充）
raise BizException(ErrorCode.ALREADY_EXISTS)

# 自定义消息
raise BizException(ErrorCode.FAIL, message="余额不足，无法扣款")

# 自定义 HTTP 状态码（默认200，需要4xx时可指定）
raise BizException(ErrorCode.FAIL, message="操作失败", http_status=400)
```

---

### 4. Pydantic 参数校验失败（自动处理，无需手动抛出）

FastAPI 的参数校验错误会被全局处理器自动拦截，响应格式如下：

```json
{
  "code": 2001,
  "message": "body -> name: Field required",
  "result": {
    "errors": [{"loc": ["body", "name"], "msg": "Field required", "type": "missing"}]
  }
}
```

---

## 三、错误码完整列表

```python
class ErrorCode(IntEnum):
    SUCCESS        = 0      # 成功
    FAIL           = -1     # 通用失败

    # 认证/授权 1xxx
    UNAUTHORIZED   = 1001   # 未登录
    TOKEN_EXPIRED  = 1002   # Token 过期
    TOKEN_INVALID  = 1003   # Token 无效
    FORBIDDEN      = 1004   # 权限不足

    # 参数校验 2xxx
    PARAMS_INVALID = 2001   # 参数不合法
    PARAMS_MISSING = 2002   # 缺少参数

    # 资源 3xxx
    NOT_FOUND      = 3001   # 资源不存在
    ALREADY_EXISTS = 3002   # 资源已存在
    RESOURCE_GONE  = 3003   # 资源已删除

    # 第三方 4xxx
    THIRD_PARTY_ERROR   = 4001
    THIRD_PARTY_TIMEOUT = 4002

    # 系统 5xxx
    INTERNAL_ERROR = 5001   # 系统内部错误
    DATABASE_ERROR = 5002   # 数据库异常
    CACHE_ERROR    = 5003   # 缓存异常
```

---

## 四、注册到 FastAPI（已在 main.py 完成）

```python
from app.exceptions import register_exception_handlers

app = FastAPI(...)
register_exception_handlers(app)  # 一行注册全部处理器
```

注册后以下异常均自动拦截并转为统一格式：
- `BizException` 及所有子类
- FastAPI/Pydantic 参数校验错误
- Starlette `HTTPException`
- 未捕获的 `Exception`（兜底，返回 500）

