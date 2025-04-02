from enum import Enum, auto
from pprint import pprint

from fastapi import Depends

from src.core.security import TokenManager
from src.core.types import ID
from src.services.cases.cache import CaseCache
from src.services.cases.dto.input import CreateCase
from src.services.cases.exc import CaseAccessDenied
from src.services.cases.repository import CaseRepository
from src.services.teams.cache import TeamCache
from src.services.teams.dependencies import is_member as is_team_member, is_administrator as is_team_administrator
from src.services.teams.repository import TeamRepository


class Action(Enum):
    CHECK_BY_CASE_ID = auto()
    CREATE = auto()
    DELETE = auto()
    GET_LIST = auto()


async def get_list_dep(
        team_id: ID,
        client_id: ID = Depends(TokenManager.decode),
        team_repository: TeamRepository = Depends(TeamRepository),
        team_cache: TeamCache = Depends(TeamCache)
):
    await is_team_member(team_id, client_id, team_repository, team_cache)


async def create_dep(model: CreateCase,
                     client_id: ID = Depends(TokenManager.decode),
                     team_repository: TeamRepository = Depends(TeamRepository),
                     team_cache: TeamCache = Depends(TeamCache)):
    await get_list_dep(model.team_id, client_id, team_repository, team_cache)


async def by_case_id_dep(case_id: ID,
                         client_id: ID = Depends(TokenManager.decode),
                         case_repository: CaseRepository = Depends(CaseRepository),
                         case_cache: CaseCache = Depends(CaseCache)):
    _is_member = await case_cache.is_team_member_in_case(case_id, case_id)
    if _is_member:
        return
    result = await case_repository.is_team_member(case_id, client_id)
    if not result:
        raise CaseAccessDenied
    await case_cache.set_team_member_for_case(client_id, case_id)


async def is_administrator(
        case_id: ID,
        client_id: ID = Depends(TokenManager.decode),
        case_repository: CaseRepository = Depends(CaseRepository),
        team_repository: TeamRepository = Depends(TeamRepository),
        case_cache: CaseCache = Depends(CaseCache),
        team_cache: TeamCache = Depends(TeamCache)
):
    administrator_id = await case_cache.get_case_admin(case_id)
    if str(administrator_id) == str(client_id):
        return
    case = await case_repository.get_document_by_id(case_id)
    await is_team_administrator(case.team.ref.id, client_id, team_cache, team_repository)


def is_member(action: Action):
    match action:
        case Action.CREATE:
            return create_dep
        case Action.DELETE:
            return is_administrator
        case Action.CHECK_BY_CASE_ID:
            return by_case_id_dep
        case Action.GET_LIST:
            return get_list_dep
