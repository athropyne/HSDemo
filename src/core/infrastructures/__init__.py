from redis.asyncio import Redis

from src.core import config
from src.core.infrastructures.mongodb import Mongo
from src.core.infrastructures.postgresql import Database
from src.core.infrastructures.redis import RedisStorage
from src.core.infrastructures.s3 import S3


database = Database()
mongodb = Mongo()
session_storage = Redis.from_url(config.settings.SESSION_STORAGE_URI)
s3_client = S3(
    config.settings.MINIO_ACCESS_KEY,
    config.settings.MINIO_SECRET_KEY,
    config.settings.MINIO_DSN,
    config.settings.MINIO_BUCKET_NAME
)
