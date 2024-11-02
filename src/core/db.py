from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)


class Database:
    def __init__(
            self,
            url: str,
            echo: bool = False,
            pool_size: int = 5,
            max_overflow: int = 10,
            pool_timeout: int = 10
    ) -> None:
        self._engine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout
        )
        self._async_session = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            expire_on_commit=False,
            autoflush=False,
        )

    @property
    async def session(self) -> AsyncSession:
        return self._async_session()
