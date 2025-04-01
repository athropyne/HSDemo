from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.core import config


class Database:
    def __init__(self):
        self.engine = create_async_engine(f"postgresql+psycopg://{config.settings.PG_DSN}", echo=True)

    async def init(self, metadata: MetaData):
        async with self.engine.connect() as connection:
            # await connection.run_sync(metadata.drop_all)
            await connection.run_sync(metadata.create_all)
            await connection.commit()
        await self.engine.dispose()

    async def dispose(self):
        await self.engine.dispose()

    def __call__(self) -> AsyncEngine:
        return self.engine
