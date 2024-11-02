from dependency_injector import containers, providers

from core.db import Database
from core.settings import settings
from core.uow import UnitOfWork
from services.auth import AuthService
from services.user import UserService
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

    uow = providers.Factory(
        UnitOfWork,
        session=db.provided.session,
    )

    auth_service = providers.Factory(
        AuthService,
        uow=uow
    )

    user_service = providers.Factory(
        UserService,
        uow=uow
    )

    auth_use_case = providers.Factory(
        AuthUseCase,
        auth_service=auth_service
    )
