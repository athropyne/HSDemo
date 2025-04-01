import aiobotocore
from aiobotocore.client import AioBaseClient
from redis.asyncio import Redis

from src.core.infrastructures import Database, database, session_storage, s3_client, S3, mongodb
from src.core.infrastructures.mongodb import Mongo


class D:
    @staticmethod
    def database() -> Database:
        return database

    @staticmethod
    def session_storage() -> Redis:
        return session_storage

    @staticmethod
    def s3() -> aiobotocore.client.AioBaseClient:
        return s3_client

    @staticmethod
    def mongo() -> Mongo:
        return mongodb
