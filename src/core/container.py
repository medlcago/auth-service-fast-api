from dependency_injector import containers, providers

from core.db import Database
from core.settings import settings
from core.uow import UnitOfWork
from services.auth import AuthService
from services.email import EmailService
from services.user import UserService
from storage.redis_store import RedisStore
from use_cases.auth.auth_use_case import AuthUseCase


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.deps",
            "api.v1.auth.router",
        ]
    )

    db = providers.Singleton(
        Database,
        url=settings.db.dsn,
        echo=settings.debug,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
        pool_timeout=settings.db.pool_timeout
    )

    redis = providers.Singleton(
        RedisStore,
        url=str(settings.redis.url)
    )

    uow = providers.Factory(
        UnitOfWork,
        session=db.provided.session,
    )

    auth_service = providers.Factory(
        AuthService,
        uow=uow,
        store=redis
    )

    user_service = providers.Factory(
        UserService,
        uow=uow
    )

    email_service = providers.Singleton(
        EmailService,
        smtp_server=settings.smtp_server.host,
        smtp_port=settings.smtp_server.port,
        smtp_user=settings.smtp_server.username,
        smtp_password=settings.smtp_server.password,
    )

    auth_use_case = providers.Factory(
        AuthUseCase,
        auth_service=auth_service,
        email_service=email_service,
    )
