import os
import dotenv
from datetime import timedelta
from pydantic import BaseSettings, validator

dotenv.load_dotenv(
    os.path.join(os.path.dirname(__file__), '../../.env')
)


class EnvBaseSettings(BaseSettings):
    class Config:
        env_file = "../../.env"


class PostgresConfig(EnvBaseSettings):
    scheme: str = "postgresql+asyncpg"
    host: str = "localhost"
    port: str = "5432"
    user: str = "postgres"
    password: str = "postgres"
    db: str = "more_tech"
    pool_size: int = 10
    pool_overflow_size: int = 10
    echo: bool = False
    autoflush: bool = False
    autocommit: bool = False
    expire_on_commit: bool = False
    engine_health_check_delay: int = 1
    url: str = ""

    class Config:
        env_prefix = "postgres_"

    @validator("url", pre=True)
    def assemble_url(cls, url: str, values: dict) -> str:
        if not url:
            url = f"{values['scheme']}://{values['user']}:{values['password']}@{values['host']}:{values['port']}/{values['db']}"
        return url


class LoggingSettings(EnvBaseSettings):
    serializer: bool = False
    level: str = "INFO"

    class Config:
        env_prefix = "logging_"


class AuthSettings(EnvBaseSettings):
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30

    class Config:
        env_prefix = "auth_"


class PolygonSettings(EnvBaseSettings):
    public_key: str = ""
    private_key: str = ""

    class Config:
        env_prefix = "polygon_"


class Settings(EnvBaseSettings):
    app_name: str = "More Tech"
    http_server_host: str = "localhost"
    http_server_port: int = 8000
    http_server_workers: int = 1
    debug: bool = False
    reload: bool = False
    db: PostgresConfig = PostgresConfig()
    logging: LoggingSettings = LoggingSettings()
    auth: AuthSettings = AuthSettings()
    polygon: PolygonSettings = PolygonSettings()



