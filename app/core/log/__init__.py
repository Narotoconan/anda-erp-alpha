from .log_loguru import register
from logging import Logger
from typing import Optional

log: Optional[Logger] = None


def register_log():
    global log
    if log is None:
        log = register()


__all__ = ['register_log', 'log']
