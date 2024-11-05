from datetime import timedelta
from pathlib import Path

from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Db(BaseModel):
    host: str
    port: int
    user: str
    password: str
    name: str
    driver: str = "asyncpg"

    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def dsn(self) -> str:
        from sqlalchemy.engine.url import URL
        return URL.create(
            drivername=f"postgresql+{self.driver}",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
            query={"async_fallback": "True"}
        ).render_as_string(hide_password=False)


class Redis(BaseModel):
    url: str


class SmtpServer(BaseModel):
    username: str
    password: str
    host: str
    port: int


class Server(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class Settings(BaseSettings):
    project_name: str = "auth-service-fast-api"

    debug: bool
    base_url: str
    base_dir: Path = Path(__file__).resolve().parent.parent.parent

    secret_key: str
    timeout: int = 30
    access_token_lifetime: timedelta = timedelta(minutes=30)
    refresh_token_lifetime: timedelta = timedelta(days=1)
    cors_origins: list[str]

    db: Db
    redis: Redis
    smtp_server: SmtpServer
    server: Server

    templates: Jinja2Templates = Jinja2Templates(directory=f"{base_dir}/templates")

    model_config = SettingsConfigDict(
        env_file=f"{base_dir}/.env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
