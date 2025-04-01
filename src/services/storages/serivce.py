from fastapi import Depends
from pydantic_core import Url

from src.core.interfaces import BaseService
from src.services.storages.dto import StorageAddInputModel
# from src.services.storages.repository import StorageRepository


# class StorageService(BaseService):
#     def __init__(self,
#                  storage_repository: StorageRepository = Depends(StorageRepository)):
#         self.storage_repository = storage_repository
#
#     async def add(self,
#                   client_id: int,
#                   model: StorageAddInputModel):
#         result = await self.storage_repository.add(model.model_dump())
#         return result
#
#     async def get_list(self, client_id: int):
#         result = await self.storage_repository.get_list()
#         return result
#
#     async def delete(self,
#                      client_id: int,
#                      storage_URL: Url):
#         result = await self.storage_repository.delete(storage_URL)
#         return result
