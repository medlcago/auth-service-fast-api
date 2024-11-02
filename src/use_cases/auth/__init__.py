from typing import Protocol

from schemas.auth import SignInSchema, SignUpSchema
from schemas.token import Token, RefreshToken


class AuthUseCaseProtocol(Protocol):
    async def login(self, schema: SignInSchema) -> Token:
        ...

    async def register(self, schema: SignUpSchema) -> Token:
        ...

    async def refresh_token(self, token: RefreshToken) -> Token:
        ...
