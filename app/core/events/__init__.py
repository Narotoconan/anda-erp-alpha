from contextlib import asynccontextmanager
from fastapi import FastAPI
from .startup import startup
from .shutdown import shutdown


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup()
    yield
    await shutdown()


__all__ = ['lifespan']
