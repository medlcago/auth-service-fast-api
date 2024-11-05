import json
import secrets
from datetime import timedelta

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
from schemas.auth import SignUpSchema, SignInSchema, ConfirmEmailSchema
from schemas.response import Status
from schemas.token import Token, RefreshToken
from storage import Store


class AuthService:
    def __init__(self, uow: IUnitOfWork, store: Store):
        self.uow = uow
        self.store = store

    async def sign_up(self, schema: SignUpSchema) -> tuple[Token, str]:
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
            await self.store.set(
                key=f"jwt:{user.id}",
                value=json.dumps(token.model_dump()),
                expire=timedelta(minutes=10)
            )
            confirmation_code = secrets.token_urlsafe(32)
            await self.store.set(
                key=confirmation_code,
                value=str(user.id),
                expire=timedelta(minutes=30)
            )
            return token, confirmation_code

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
            token_cache = await self.store.get(key=f"jwt:{user.id}")
            if token_cache:
                token = Token.model_validate(json.loads(token_cache))
                return token
            token = self.get_token(user_id=user.id)
            await self.store.set(
                key=f"jwt:{user.id}",
                value=json.dumps(token.model_dump()),
                expire=timedelta(minutes=10)
            )
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

    async def confirm_email(self, data: ConfirmEmailSchema) -> Status:
        user_id = await self.store.get(key=data.code)
        if not user_id:
            raise InvalidCredentialsException
        async with self.uow:
            user = await self.uow.user_repository.update(int(user_id), is_active=True)
            if not user:
                raise InvalidCredentialsException
        await self.store.delete(key=data.code)
        return Status(
            ok=True
        )
