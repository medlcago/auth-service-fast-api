from fastapi import APIRouter

from api.v1.auth import router as auth_router
from api.v1.users import router as users_router

__all__ = (
    "v1",
)

v1 = APIRouter(prefix="/v1")
v1.include_router(auth_router)
v1.include_router(users_router)
