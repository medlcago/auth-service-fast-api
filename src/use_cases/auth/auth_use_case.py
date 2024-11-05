from core.settings import settings
from schemas.auth import SignInSchema, SignUpSchema, ConfirmEmailSchema
from schemas.response import Status
from schemas.token import RefreshToken, Token
from services.auth import AuthServiceProtocol
from services.email import EmailServiceProtocol


class AuthUseCase:
    def __init__(
            self,
            auth_service: AuthServiceProtocol,
            email_service: EmailServiceProtocol,
    ):
        self.auth_service = auth_service
        self.email_service = email_service

    async def login(self, schema: SignInSchema) -> Token:
        token = await self.auth_service.sign_in(schema=schema)
        return token

    async def register(self, schema: SignUpSchema) -> Token:
        token, confirmation_code = await self.auth_service.sign_up(schema=schema)
        await self.email_service.send_confirmation_email(
            to_email=str(schema.email),
            from_email=settings.smtp_server.username,
            subject="Confirm your email",
            code=confirmation_code
        )
        return token

    async def refresh_token(self, token: RefreshToken) -> Token:
        token = await self.auth_service.refresh_token(token=token)
        return token

    async def confirm_email(self, data: ConfirmEmailSchema) -> Status:
        status = await self.auth_service.confirm_email(data=data)
        return status
