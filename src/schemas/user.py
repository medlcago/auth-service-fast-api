from pydantic import BaseModel, EmailStr


class ReadUserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
