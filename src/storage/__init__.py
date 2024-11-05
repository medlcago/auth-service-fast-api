from abc import ABC, abstractmethod
from datetime import timedelta
from typing import TypeVar, Optional

_ExpireType = TypeVar("_ExpireType", bound=float | timedelta | None)


class Store(ABC):
    @abstractmethod
    async def set(self, key: str, value: str, expire: _ExpireType = None):
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str):
        raise NotImplementedError

    @abstractmethod
    async def exists(self, key: str) -> bool:
        raise NotImplementedError
