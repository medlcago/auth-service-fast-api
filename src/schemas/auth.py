from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class SignUpSchema(BaseModel):
    username: Annotated[str, Field(pattern=r"^[a-zA-Z0-9_]{5,32}$")]
    email: EmailStr
    password: Annotated[str, Field(min_length=6, max_length=60)]


class SignInSchema(BaseModel):
    username: str
    password: str


class ConfirmEmailSchema(BaseModel):
    code: str
