from fastapi import Depends
from loguru import logger

from src.core.security import TokenManager
from src.core.types import ID, ReplyMode
from src.services.teams.cache import TeamCache
from src.services.teams.exc import YouNotAdministrator, DeleteAdministratorError, TeamNotFound, YouNotTeamMember
from src.services.teams.repository import TeamRepository


async def is_administrator(
        team_id: ID,
        client_id: ID = Depends(TokenManager.decode),
        cache: TeamCache = Depends(TeamCache),
        team_repository: TeamRepository = Depends(TeamRepository)
):
    logger.debug(f"Получаем id администратора команды {team_id}")
    administrator_id = await cache.get_team_admin(team_id)

    if administrator_id is not None:
        logger.debug(f"Данные об администраторе {administrator_id} команды {team_id} взяты из кэша")
        if str(administrator_id) != str(client_id):
            logger.debug(f"Пользователь {client_id} не является администратором команды {team_id}")
            raise YouNotAdministrator
        return

    logger.debug(f"Данные о команде {team_id} отсутствуют в кэше")
    logger.debug(f"Попытка получения информации о команде {team_id} из базы")
    try:
        team = await team_repository.get_by_id(team_id, ReplyMode.SHORT)
        logger.debug(f"данные о команде {team_id} получены из базы")
        if team.administrator.id != client_id:
            logger.debug(f"Пользователь {client_id} не является администратором команды {team_id}")
            raise YouNotAdministrator
        logger.debug(f"Добавляем администратора {client_id} для команды {team_id} в кэш")
        await cache.set_team_admin(client_id, team_id)
    except TeamNotFound:
        logger.debug(f"Команда {team_id} не найдена")
        raise


def protect_administrator(
        member_id: ID,
        client_id: ID = Depends(TokenManager.decode)
):
    """Защищает администратора команды от удаления самого себя"""
    if member_id == client_id:
        raise DeleteAdministratorError


async def is_member(
        team_id: ID,
        client_id: ID = Depends(TokenManager.decode),
        team_repository: TeamRepository = Depends(TeamRepository),
        cache: TeamCache = Depends(TeamCache)
):
    _is_member = await cache.is_team_member(team_id, client_id)
    if _is_member:
        logger.debug(f"Пользователь {client_id} является участником команды {team_id}. Данные получены из кэша.")
        return
    _is_member = await team_repository.is_team_member(team_id, client_id)
    if not _is_member:
        logger.debug(f"Пользователь {client_id} не является участником команды {team_id}")
        raise YouNotTeamMember
    logger.debug(f"Пользователь {client_id} является участником команды {team_id}. Данные получены из базы")
    await cache.add_team_member(client_id, team_id)


async def is_member_only(
        team_id: ID,
        client_id: ID = Depends(TokenManager.decode),
        team_repository: TeamRepository = Depends(TeamRepository),
        cache: TeamCache = Depends(TeamCache)
):
    try:
        await is_administrator(team_id, client_id, cache, team_repository)
        raise DeleteAdministratorError
    except YouNotAdministrator:
        await is_member(team_id, client_id, team_repository, cache)
