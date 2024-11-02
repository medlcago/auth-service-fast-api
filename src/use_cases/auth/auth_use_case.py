from schemas.auth import SignInSchema, SignUpSchema
from schemas.token import RefreshToken, Token
from services.auth import AuthServiceProtocol


class AuthUseCase:
    def __init__(self, auth_service: AuthServiceProtocol):
        self.auth_service = auth_service

    async def login(self, schema: SignInSchema) -> Token:
        token = await self.auth_service.sign_in(schema=schema)
        return token

    async def register(self, schema: SignUpSchema) -> Token:
        token = await self.auth_service.sign_up(schema=schema)
        return token

    async def refresh_token(self, token: RefreshToken) -> Token:
        token = await self.auth_service.refresh_token(token=token)
        return token
