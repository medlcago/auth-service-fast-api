from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from schemas.user import ReadUserSchema


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=False, server_default="0")
    is_admin: Mapped[bool] = mapped_column(default=False, server_default="0")

    def to_read_model(self) -> ReadUserSchema:
        return ReadUserSchema.model_validate(self, from_attributes=True)
