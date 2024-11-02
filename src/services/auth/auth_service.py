from core.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException
)
from core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    get_identity
)
from core.uow import IUnitOfWork
from schemas.auth import SignUpSchema, SignInSchema
from schemas.token import Token, RefreshToken


class AuthService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def sign_up(self, schema: SignUpSchema) -> Token:
        async with self.uow:
            already_exists = await self.uow.user_repository.get_by_username_or_email(
                username=schema.username,
                email=schema.email
            )
            if already_exists:
                raise UserAlreadyExistsException
            schema.password = hash_password(password=schema.password)
            user = await self.uow.user_repository.create(create_object=schema)
            token = self.get_token(user_id=user.id)
            return token

    async def sign_in(self, schema: SignInSchema) -> Token:
        async with self.uow:
            user = await self.uow.user_repository.get_by_username_or_email(
                username=schema.username,
                email=schema.username
            )
            if not user:
                raise InvalidCredentialsException
            if not verify_password(password=schema.password, hashed_password=user.password):
                raise InvalidCredentialsException
            token = self.get_token(user_id=user.id)
            return token

    @staticmethod
    def get_token(user_id: int) -> Token:
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh_token(self, token: RefreshToken) -> Token:
        user_id = get_identity(token=token.refresh_token, token_type="refresh")
        if not user_id:
            raise InvalidCredentialsException
        return self.get_token(user_id=user_id)
