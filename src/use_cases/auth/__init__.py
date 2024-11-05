from typing import Protocol

from schemas.auth import SignInSchema, SignUpSchema, ConfirmEmailSchema
from schemas.response import Status
from schemas.token import Token, RefreshToken


class AuthUseCaseProtocol(Protocol):
    async def login(self, schema: SignInSchema) -> Token:
        ...

    async def register(self, schema: SignUpSchema) -> Token:
        ...

    async def refresh_token(self, token: RefreshToken) -> Token:
        ...

    async def confirm_email(self, data: ConfirmEmailSchema) -> Status:
        ...
