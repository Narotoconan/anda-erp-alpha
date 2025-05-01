from fastapi import APIRouter, FastAPI

from app.api.user import router_user


def register_router(app: FastAPI):
    router = APIRouter()
    router.include_router(router_user)

    app.include_router(router)


__all__ = ["register_router"]
