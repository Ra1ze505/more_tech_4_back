import os
import dotenv
from pydantic import BaseSettings

dotenv.load_dotenv(
    os.path.join(os.path.dirname(__file__), '.env')
)


class EnvBaseSettings(BaseSettings):
    class Config:
        env_file = ".env"


class PostgresConfig(EnvBaseSettings):
    host: str = "localhost"
    port: str = "5432"
    user: str = "postgres"
    password: str = "postgres"
    db: str = "more_tech"
    url: str = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

    class Config:
        env_prefix = "db_"


class Settings(EnvBaseSettings):
    http_server_host: str = "localhost"
    http_server_port: int = 8000
    http_server_workers: int = 1
    debug: bool = False
    reload: bool = False
    db: PostgresConfig = PostgresConfig()


settings = Settings()
