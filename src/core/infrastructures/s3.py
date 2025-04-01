from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from pydantic_core import Url


class S3:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: Url,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def __call__(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def create_bucket(self, bucket_name: str):
        async with self() as client:
            try:
                await client.head_bucket(Bucket=bucket_name)
                return True
            except ClientError as e:
                await client.create_bucket(Bucket=bucket_name)

    async def upload(self,
                     file_name: str,
                     file_data: bytes,
                     content_type: str
                     ):
        async with self() as client:
            result = await client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=file_data,
                ContentType=content_type
            )
            return result

    async def get_object(self,
                         object_key: str,
                         chunk_size: int = 1024 * 1024
                         ):
        async with self() as client:
            try:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_key)
                stream = response['Body']

                while True:
                    chunk = await stream.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
            except Exception as e:
                print(f"Error getting object: {e}")
                raise e
