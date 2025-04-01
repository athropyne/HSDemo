from fastapi import APIRouter, Depends
from starlette import status

from src.core.security import TokenManager
from src.core.types import ID, ReplyMode, IDModel
from src.services.cases.dependencies import is_member, is_administrator
from src.services.cases.dto.input import CreateCase, UpdateCase
from src.services.cases.dto.output import CaseFullInfo, CaseShortInfo
from src.services.cases.service import CaseService

case_router = APIRouter(prefix="/cases", tags=["Случаи"])
output_types = CaseFullInfo | CaseShortInfo | IDModel

@case_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый случай",
    description="Создает новый случай. Доступно только участнику команды",
    dependencies=[Depends(is_member)],
    response_model=output_types
)
async def create(
        model: CreateCase,
        output_mode: ReplyMode = ReplyMode.SHORT,
        client_id: ID = Depends(TokenManager.decode),
        service: CaseService = Depends(CaseService)
):
    return await service.create(client_id, model, output_mode)


@case_router.put(
    "/{case_id}",
    status_code=status.HTTP_200_OK,
    summary="Изменить случай",
    description="Обновляет случай. Доступно только участнику команды",
    dependencies=[Depends(is_member)],
    response_model=output_types
)
async def update(
        case_id: ID,
        model: UpdateCase,
        output_mode: ReplyMode = ReplyMode.ID,
        client_id: ID = Depends(TokenManager.decode),
        service: CaseService = Depends(CaseService)
):
    return await service.update(client_id, case_id, model,output_mode)


@case_router.get(
    "/{case_id}",
    status_code=status.HTTP_200_OK,
    summary="Получить случай по идентификатору",
    description="Возвращает случай по идентификатору. Доступно только участнику команды",
    dependencies=[Depends(id_member)],
    response_model=output_types
)
async def get_by_id(
        case_id: ID,
        output_mode: ReplyMode = ReplyMode.FULL,
        client_id: ID = Depends(TokenManager.decode),
        service: CaseService = Depends(CaseService)
):
    return await service.get_by_id(client_id, case_id, output_mode)


@case_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Получить список случаев",
    description="Возвращает список случаев в команде. Доступно только участникам команды",
    dependencies=[Depends(is_member)],
    response_model=list[output_types]
)
async def get_list(
        team_id: ID,
        skip: int = 0,
        limit: int = 30,
        output_mode: ReplyMode = ReplyMode.SHORT,
        client_id: ID = Depends(TokenManager.decode),
        service: CaseService = Depends(CaseService)
):
    return await service.get_list(client_id, team_id, skip, limit, output_mode)


@case_router.delete(
    "/{case_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить случай по идентификатору",
    description="Удаляет случай по идентификатору. Доступно только администратору команды",
    dependencies=[Depends(is_administrator)]
)
async def delete(
        case_id: ID,
        client_id: ID = Depends(TokenManager.decode),
        service: CaseService = Depends(CaseService)
):
    await service.delete(client_id, case_id)
