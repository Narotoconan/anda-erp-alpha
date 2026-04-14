"""Cache decorators for simple function result caching"""
import functools
import inspect
import hashlib
import json
from typing import Any, Callable, Optional
from app.core.cache.redis import get_redis_manager


def cache(key_prefix: str = "", ttl: Optional[int] = None) -> Callable:
    """Async function result cache decorator with TTL support"""
    def decorator(func: Callable) -> Callable:
        if not inspect.iscoroutinefunction(func):
            raise RuntimeError(f"Cache decorator only supports async functions")

        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            cache_key = _generate_cache_key(func, key_prefix, args, kwargs)
            redis_manager = get_redis_manager()

            cached = await redis_manager.get(cache_key)
            if cached is not None:
                return cached

            result = await func(*args, **kwargs)
            await redis_manager.set(cache_key, result, ex=ttl)
            return result

        return wrapper
    return decorator


def _generate_cache_key(func: Callable, prefix: str, args: tuple, kwargs: dict) -> str:
    """Generate cache key from function name and parameters"""
    func_name = func.__name__
    key_base = f"{prefix}:{func_name}" if prefix else func_name
    params = json.dumps({"args": args, "kwargs": kwargs}, default=str, sort_keys=True)
    param_hash = hashlib.md5(params.encode()).hexdigest()[:8]
    return f"cache:{key_base}:{param_hash}"


__all__ = ['cache']

