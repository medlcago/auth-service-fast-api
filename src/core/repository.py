from typing import Self, Type, TypeVar, Generic, Optional

from pydantic import BaseModel
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType]):
    model_type: Type[ModelType]

    def __init__(self: Self, session: AsyncSession) -> None:
        self.session = session

    async def get(self: Self, _id: int) -> ModelType | None:
        stmt = select(self.model_type).filter_by(id=_id)
        return await self.session.scalar(stmt)

    async def get_by_ids(self: Self, ids: list[int]) -> list[ModelType]:
        stmt = select(self.model_type).where(self.model_type.id.in_(ids))
        models = (await self.session.scalars(stmt)).all()
        return list(models)

    async def create(self: Self, create_object: CreateSchemaType) -> ModelType:
        stmt = (
            insert(self.model_type).values(**create_object.model_dump()).returning(self.model_type)
        )
        return await self.session.scalar(stmt)

    async def delete(self, _id: int) -> bool:
        stmt = delete(self.model_type).filter_by(id=_id)
        await self.session.execute(stmt)
        return True

    async def filter_by(self, many: bool = False, **kwargs) -> Optional[ModelType] | list[ModelType]:
        stmt = select(self.model_type).filter_by(**kwargs)
        if many:
            return list((await self.session.scalars(stmt)).all())
        return await self.session.scalar(stmt)
