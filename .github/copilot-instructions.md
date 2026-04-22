# 项目开发规范 (Copilot Instructions)

## 1. 技术栈上下文
- **语言/框架**: Python 3.12, FastAPI
- **目录结构**: 遵循标准的 app/ 架构，项目配置位于config/，业务逻辑位于 app/services
- **包管理器**: 项目使用UV进行包管理，在项目的虚拟环境中运行

## 2. 核心编码规范
### 日志处理 (Logging)
- **禁止**: 严禁使用 `print()` 或原生 `logging` 库。
- **规范**: 必须使用项目封装的统一日志工具。
- **导入**: `from app.core.log import log`
- **用法**: 仅允许使用 `log.info()`, `log.error()`, `log.warning()`, `log.debug()`

### 异常处理 (Exception Handling)
- 业务异常需抛出 `app.core.exceptions` 中的自定义异常。
- 必须包含具体的错误原因描述。

## 3. 命名与注释
- 函数必须包含 类型提示 (Type Hints)。
- 关键业务逻辑必须编写中文 docstring。