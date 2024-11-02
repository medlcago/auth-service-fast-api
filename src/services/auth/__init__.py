from typing import Protocol

from schemas.auth import SignUpSchema, SignInSchema
from schemas.token import Token, RefreshToken
from services.auth.auth_service import AuthService


class AuthServiceProtocol(Protocol):
    async def sign_up(self, schema: SignUpSchema) -> Token:
        ...

    async def sign_in(self, schema: SignInSchema) -> Token:
        ...

    @staticmethod
    def get_token(user_id: int) -> Token:
        ...

    async def refresh_token(self, token: RefreshToken) -> Token:
        ...
