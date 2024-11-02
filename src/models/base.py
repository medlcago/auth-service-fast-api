from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from core.settings import settings


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    metadata = MetaData(
        naming_convention=settings.db.naming_convention
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__}s".lower()
