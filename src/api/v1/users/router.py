from fastapi import APIRouter
from fastapi_cache.decorator import cache

from api.deps import CurrentUserDep
from schemas.user import ReadUserSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=ReadUserSchema)
@cache(expire=60)
async def get_me(user: CurrentUserDep):
    return user
