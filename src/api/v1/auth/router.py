from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, status, Depends

from api.deps import OAuth2FormDep
from core.container import Container
from schemas.auth import SignInSchema, SignUpSchema, ConfirmEmailSchema
from schemas.response import Status
from schemas.token import Token, RefreshToken
from use_cases.auth import AuthUseCaseProtocol

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/sign-up", response_model=Token, status_code=status.HTTP_201_CREATED)
@inject
async def sign_up(
        schema: SignUpSchema,
        auth_use_case: AuthUseCaseProtocol = Depends(Provide[Container.auth_use_case])
) -> Token:
    return await auth_use_case.register(schema=schema)


@router.post("/sign-in", response_model=Token)
@inject
async def sign_in(
        form_data: OAuth2FormDep,
        auth_use_case: AuthUseCaseProtocol = Depends(Provide[Container.auth_use_case])
):
    schema = SignInSchema(
        username=form_data.username,
        password=form_data.password
    )
    return await auth_use_case.login(schema=schema)


@router.post("/refresh", response_model=Token)
@inject
async def refresh_token(
        token: RefreshToken,
        auth_use_case: AuthUseCaseProtocol = Depends(Provide[Container.auth_use_case])
):
    return await auth_use_case.refresh_token(token=token)


@router.post("/confirm-email/", response_model=Status)
@inject
async def confirm_email(
        data: ConfirmEmailSchema,
        auth_use_case: AuthUseCaseProtocol = Depends(Provide[Container.auth_use_case])
):
    response = await auth_use_case.confirm_email(data=data)
    return response
