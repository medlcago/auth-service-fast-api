from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from repo import UserRepository


class IUnitOfWork(ABC):
    user_repository: UserRepository

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...

    @abstractmethod
    async def close(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.user_repository = UserRepository(session=self._session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.close()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def close(self):
        await self._session.close()
