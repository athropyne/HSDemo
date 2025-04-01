from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.core import config
from src.core.schemas import User, Team, Material, Case, Storage


class Mongo:
    def __init__(self):
        self.client = AsyncIOMotorClient(config.settings.MONGO_DSN)

    async def init(self):
        # await self.client.drop_database(self.client.RusByte)
        await init_beanie(database=self.client.HSDemo,
                          document_models=[
                              User,
                              Team,
                              Material,
                              Case,
                              Storage,
                          ])
