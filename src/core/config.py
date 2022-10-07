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


# class Settings(object):
#     # Server
#     HTTP_SERVER_HOST = os.environ.get("HTTP_SERVER_HOST")
#     HTTP_SERVER_PORT = int(os.environ.get("HTTP_SERVER_PORT"))
#     COUNT_WORKERS_UVICORN = int(os.environ.get("COUNT_WORKERS_UVICORN", 1))
#
#     # PostgreSQL
#     DB_HOST = os.environ.get("DB_HOST")
#     DB_PORT = int(os.environ.get("DB_PORT"))
#     DB_USER = os.environ.get("DB_USER")
#     DB_PASSWORD = os.environ.get("DB_PASSWORD")
#     DATABASE = os.environ.get("DATABASE")
#
#     DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}"
#
#     # На данный момент отключил за ненадобностью, так как получилось перевести часть логики на запрос к БД.
#     # Redis
#     # REDIS_HOST = f"""redis://{os.environ.get("REDIS_HOST")}"""
#     # REDIS_PORT = int(os.environ.get("REDIS_PORT"))
#     # REDIS_ZONE_INFO_DB = int(os.environ.get("REDIS_ZONE_INFO_DB"))
# #
#     # Redis cache
#     # CACHE_ZONE_KEY = os.environ.get("CACHE_ZONE_KEY")
