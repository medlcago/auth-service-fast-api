from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from api import api_router
from core.container import Container
from core.exceptions import APIException
from core.exceptions import api_exception_handler
from core.logger import logger
from core.settings import settings


class APIServer:
    def __init__(self) -> None:
        self.app = FastAPI(
            title=settings.project_name,
            docs_url="/docs",
            openapi_url="/docs.json",
            lifespan=self.lifespan
        )

    @asynccontextmanager
    async def lifespan(self, _: FastAPI) -> AsyncIterator[None]:
        if settings.debug:
            backend = InMemoryBackend()
            logger.info("[FastAPICache]: Using in-memory cache...")
        else:
            redis = aioredis.from_url(url=settings.redis.url)
            await redis.ping()
            backend = RedisBackend(redis)
            logger.info("[FastAPICache]: Using Redis cache...")
        FastAPICache.init(backend, prefix="fastapi-cache")
        yield

    def _build_app(self) -> FastAPI:
        container = Container()
        self.app.container = container

        @self.app.get("/health_check")
        async def health_check():
            return {
                "status": "ok",
            }

        if settings.cors_origins:
            self.app.add_middleware(
                CORSMiddleware,  # noqa
                allow_origins=settings.cors_origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        self.app.add_exception_handler(APIException, api_exception_handler)  # noqa
        self.app.include_router(api_router)
        return self.app

    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        import uvicorn
        app = self._build_app()
        uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    server = APIServer()
    server.run(
        host=settings.server.host,
        port=settings.server.port,
    )
