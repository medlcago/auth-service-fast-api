from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class Token(AccessToken, RefreshToken):
    token_type: str = "Bearer"
