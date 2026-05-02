from logging import Logger

from .log_loguru import register

log: Logger


def register_log():
    global log
    if log is None:
        log = register()


__all__ = ["log", "register_log"]
