from fastapi import APIRouter, Depends, Body
from starlette import status

from src.core.security import TokenManager
from src.core.types import ID
from src.services.members.service import TeamMemberService
from src.services.teams.dependencies import is_administrator, protect_administrator, is_member, is_member_only

team_member_router = APIRouter(prefix="/{team_id}/members", tags=["Участники команд"])


@team_member_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Добавить участника",
    description="Добавляет участника в команду. Доступно только администратору",
    dependencies=[Depends(is_administrator)]
)
async def add(
        team_id: ID,
        member_id: ID = Body(...),
        client_id: ID = Depends(TokenManager.decode),
        service: TeamMemberService = Depends(TeamMemberService)
):
    return await service.add(client_id, team_id, member_id)


@team_member_router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить участника",
    description="Удаляет участника из команды. Доступно только администратору",
    dependencies=[Depends(protect_administrator), Depends(is_administrator)]
)
async def remove(
        team_id: ID,
        member_id: ID,
        client_id: ID = Depends(TokenManager.decode),
        service: TeamMemberService = Depends(TeamMemberService)
):
    return await service.remove(client_id, team_id, member_id)


@team_member_router.patch(
    "/exit",
    status_code=status.HTTP_200_OK,
    summary="Выйти из команды",
    description="Выход из команды. Доступно любому участнику команды кроме администратора",
    dependencies=[Depends(is_member_only)]
)
async def get_team_member_list(
        team_id: ID,
        client_id: ID = Depends(TokenManager.decode),
        service: TeamMemberService = Depends(TeamMemberService)
):
    return await service.exit(client_id, team_id)
