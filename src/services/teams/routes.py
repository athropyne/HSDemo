from typing import Union

from fastapi import APIRouter, Depends
from starlette import status

from src.core.security import TokenManager
from src.core.types import ID, ReplyMode
from src.services.teams.dependencies import is_administrator, is_member
from src.services.teams.dto.input import CreateTeam, UpdateTeam
from src.services.teams.dto.output import TeamFullInfo, TeamShortInfo, IDModel
from src.services.teams.service import TeamService

team_router = APIRouter(prefix="/teams", tags=["Команды"])
__reply_type = Union[TeamFullInfo, TeamShortInfo, IDModel]


@team_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать команду",
    description="Создает команду и добавляет в создателя в качестве участника команды с ролью администратора.",
    response_model=Union[TeamFullInfo, TeamShortInfo, IDModel]
)
async def create(
        model: CreateTeam,
        output_mode: ReplyMode = ReplyMode.SHORT,
        client_id: ID = Depends(TokenManager.decode),
        service: TeamService = Depends(TeamService)
):
    return await service.create(client_id, model, output_mode)


@team_router.put(
    "/{team_id}",
    status_code=status.HTTP_200_OK,
    summary="Изменить данные команды",
    description="Обновляет данные команды. Доступно только для администратора команды",
    response_model=Union[TeamFullInfo, TeamShortInfo, IDModel],
    dependencies=[Depends(is_administrator)]
)
async def update(
        team_id: ID,
        model: UpdateTeam,
        output_mode: ReplyMode = ReplyMode.FULL,
        client_id: ID = Depends(TokenManager.decode),
        service: TeamService = Depends(TeamService)
):
    return await service.update(client_id, team_id, model, output_mode)


@team_router.get(
    "/{team_id}",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о команде",
    description="Возвращает все данные о команде с участниками. Доступно только участнику команды",
    response_model=Union[TeamFullInfo, TeamShortInfo, IDModel],
    dependencies=[Depends(is_member)]
)
async def get_by_id(
        team_id: ID,
        output_mode: ReplyMode = ReplyMode.FULL,
        client_id: int = Depends(TokenManager.decode),
        service: TeamService = Depends(TeamService)
):
    return await service.get_by_id(client_id, team_id, output_mode)


@team_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Получить список команд",
    description="Возвращает список команд в которых пользователь является участником",
    response_model=list[Union[TeamFullInfo, TeamShortInfo, IDModel]]
)
async def get_list(
        skip: int = 0,
        limit: int = 30,
        output_mode: ReplyMode = ReplyMode.SHORT,
        client_id: ID = Depends(TokenManager.decode),
        service: TeamService = Depends(TeamService)
):
    return await service.get_list(client_id, skip, limit, output_mode)


@team_router.delete(
    "/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить команду",
    description="Удаляет команду. Доступно только для администратора команды",
    dependencies=[Depends(is_administrator)],
    responses={204: {"description": "успешно удален"}}
)
async def delete(
        team_id: ID,
        client_id: ID = Depends(TokenManager.decode),
        service: TeamService = Depends(TeamService)
):
    return await service.delete(client_id, team_id)
