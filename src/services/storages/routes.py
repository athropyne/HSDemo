from fastapi import APIRouter, Depends
from pydantic_core import Url
from starlette import status

from src.core.security import TokenManager
from src.services.storages.dto import StorageAddInputModel
# from src.services.storages.serivce import StorageService

storage_router = APIRouter(prefix="/storages", tags=["Удаленные хранилища"])


@storage_router.post(
    "/",
    summary="Добавить внешнее хранилище",
    status_code=status.HTTP_201_CREATED
)
async def add(
        model: StorageAddInputModel,
        client_id: int = Depends(TokenManager.decode),
        # service: StorageService = Depends(StorageService)
):
    return await service.add(client_id, model)


@storage_router.get(
    "/",
    summary="Получить все адреса внешних хранилищ",
    status_code=status.HTTP_200_OK
)
async def get_list(
        client_id: int = Depends(TokenManager.decode),
        # service: StorageService = Depends(StorageService)
):
    return await service.get_list(client_id)


@storage_router.delete(
    "/{storage_URL}",
    summary="Удалить внешнее хранилище",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
        storage_URL: Url,
        client_id: int = Depends(TokenManager.decode),
        # service: StorageService = Depends(StorageService)
):
    return await service.delete(client_id, storage_URL)
