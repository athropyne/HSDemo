from uuid import UUID

from fastapi import APIRouter, UploadFile, Depends
from starlette import status

from src.core.security import TokenManager
from src.services.materials.dependencies import build_create_model
from src.services.materials.dto import MaterialAddInputModel, MaterialUpdateInputModel
from src.services.materials.service import MaterialService

material_router = APIRouter(prefix="/materials", tags=["Материалы"])


@material_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Добавить материал",
    description="Добавляет новый материал в случай"
)
async def create(
        file: UploadFile,
        model: MaterialAddInputModel = Depends(build_create_model),
        client_id: int = Depends(TokenManager.decode),
        service: MaterialService = Depends(MaterialService)
):
    return await service.create(client_id, file, model)


@material_router.put(
    "/{material_id}"
)
async def update(
        material_id: UUID ,
        model: MaterialUpdateInputModel,
        client_id: int = Depends(TokenManager.decode),
        service: MaterialService = Depends(MaterialService)
):
    return await service.update(client_id, material_id, model)


@material_router.get(
    "/{case_id}"
)
async def get_list(
        case_id: int,
        client_id: int = Depends(TokenManager.decode),
        service: MaterialService = Depends(MaterialService)
):
    await service.get_list(client_id, case_id)

#
# @material_router.get(
#     "/{material_id}"
# )
# async def get_by_id(
#         material_id: int,
#         client_id: int = Depends(TokenManager.decode),
#         service: MaterialService = Depends(MaterialService)
# ):
#     return await service.get_list(client_id, material_id)


@material_router.delete(
    "/{material_id}"
)
async def delete(
        material_id: UUID,
        client_id: int = Depends(TokenManager.decode),
        service: MaterialService = Depends(MaterialService)
):
    return await service.delete(client_id, material_id)
