import sys

from loguru import logger

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


def is_dev(dev=False):
    if not dev:
        load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')

    # server
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000

    # # admin
    ADMINISTRATOR_LOGIN: str = "admin@example.com"
    ADMINISTRATOR_PASSWORD: str = "admin"

    # databases
    PG_DSN: str = "postgres:postgres@localhost:5432/HSDemo"
    MONGO_DSN: str = "mongodb://localhost:27017"

    # minio
    MINIO_DSN: str = "http://127.0.0.1:9000"
    MINIO_ACCESS_KEY: str = "llbRX1XkLkeRA0d0HjFZ"
    MINIO_SECRET_KEY: str = "wHSq4DTbvymLxAjQ658JMCp5MW32iUuaKTi9ShPr"
    MINIO_BUCKET_NAME: str = "files"

    # token config
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_HOURS: int = 24 * 15
    TOKEN_SECRET_KEY: str = "abracadabra"

    # brokers
    BROKER_URI: str = "amqp://guest:guest@localhost:5672/"

    # authenticated users storage
    SESSION_STORAGE_URI: str = "redis://localhost:6379/0"


settings = Settings()
logger.add(sys.stderr,
           colorize=True,
           format="<green>{time}</green> <blue>{level}</blue> {message}",
           filter="my_module",
           level="DEBUG")

