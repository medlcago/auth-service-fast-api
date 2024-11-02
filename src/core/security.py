from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Any, Literal

import bcrypt
import jwt
from fastapi.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.exceptions import InvalidCredentialsException
from core.settings import settings

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(
        password=password.encode("utf-8"),
        salt=salt
    )
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8")
    )


def create_token(
        identity: int,
        token_type: Literal["access", "refresh"],
        claims: dict[str, Any] = None
) -> str:
    lifetime = {
        "access": settings.access_token_lifetime,
        "refresh": settings.refresh_token_lifetime,
    }
    payload = {
        "sub": identity,
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC) + lifetime[token_type],
        "token_type": token_type,
    }
    payload.update(claims or {})

    token = jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm=ALGORITHM,

    )
    return token


def create_access_token(
        identity: int,
        claims: dict[str, Any] = None
) -> str:
    return create_token(identity=identity, token_type="access", claims=claims)


def create_refresh_token(
        identity: int,
        claims: dict[str, Any] = None
) -> str:
    return create_token(identity=identity, token_type="refresh", claims=claims)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload
    except jwt.PyJWTError:
        return {}


def get_identity(token: str, token_type: str | None = None) -> int | None:
    payload = decode_token(token=token)
    if not (payload and payload.get("sub")):
        return
    if token_type and payload.get("token_type") != token_type:
        return
    return payload.get("sub")


@dataclass
class Credentials:
    token: str
    token_type: str
    identity: int


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, token_type: str = "access"):
        super().__init__(auto_error=auto_error)
        self.token_type = token_type

    async def __call__(self, request: Request) -> Credentials:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise InvalidCredentialsException
        identity = get_identity(token=credentials.credentials, token_type=self.token_type)
        if not identity:
            raise InvalidCredentialsException
        return Credentials(
            token=credentials.credentials,
            token_type=self.token_type,
            identity=identity
        )
