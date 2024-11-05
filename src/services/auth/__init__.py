from typing import Protocol

from schemas.auth import SignUpSchema, SignInSchema, ConfirmEmailSchema
from schemas.response import Status
from schemas.token import Token, RefreshToken
from services.auth.auth_service import AuthService


class AuthServiceProtocol(Protocol):
    async def sign_up(self, schema: SignUpSchema) -> tuple[Token, str]:
        ...

    async def sign_in(self, schema: SignInSchema) -> Token:
        ...

    @staticmethod
    def get_token(user_id: int) -> Token:
        ...

    async def refresh_token(self, token: RefreshToken) -> Token:
        ...

    async def confirm_email(self, data: ConfirmEmailSchema) -> Status:
        ...
