from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.container import Container
from core.exceptions import InvalidCredentialsException
from core.security import JWTBearer, Credentials
from schemas.user import ReadUserSchema
from services.user import UserServiceProtocol

jwt_bearer = JWTBearer()

JwtBearerDep = Annotated[Credentials, Depends(jwt_bearer)]

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/sign-in"
)

OAuth2Dep = Annotated[str, Depends(oauth2_scheme)]

OAuth2FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@inject
async def get_current_user(
        credentials: JwtBearerDep,
        user_service: UserServiceProtocol = Depends(Provide[Container.user_service]),
) -> ReadUserSchema:
    user = await user_service.get_user(user_id=credentials.identity)
    if not user:
        raise InvalidCredentialsException
    return user.to_read_model()


CurrentUserDep = Annotated[ReadUserSchema, Depends(get_current_user)]
