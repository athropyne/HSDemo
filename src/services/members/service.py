from fastapi import Depends
from loguru import logger

from src.core.exc import NotFound
from src.core.interfaces import BaseService
from src.core.types import ID
from src.services.members.exc import TeamMemberAlreadyExists
from src.services.members.repository import TeamMemberRepository
from src.services.teams.cache import TeamCache
from src.services.teams.exc import TeamNotFound
from src.services.users.exc import UserNotFound


class TeamMemberService(BaseService):
    def __init__(self,
                 team_member_repository: TeamMemberRepository = Depends(TeamMemberRepository),
                 cache: TeamCache = Depends(TeamCache)):
        self.cache = cache
        self.team_member_repository = team_member_repository

    async def add(self, client_id: ID, team_id: ID, member_id: ID):
        try:
            logger.debug(f"Попытка пользователя {client_id} добавить участника {member_id} в команду {team_id}")
            result = await self.team_member_repository.add(team_id, member_id)
            return result
        except TeamMemberAlreadyExists:
            logger.debug(f"Пользователь {member_id} уже участник команды {team_id}")
            raise
        except UserNotFound:
            logger.debug(f"Пользователь {member_id} не найден в системе")
            raise
        except TeamNotFound:
            logger.debug(f"Команда {team_id} не найдена в системе")
            raise

    async def remove(self,
                     client_id: ID,
                     team_id: ID,
                     member_id: ID):
        try:
            logger.debug(f"Попытка пользователя {client_id} удалить участника {member_id} из команды {team_id}")
            result = await self.team_member_repository.remove(team_id, member_id)
            await self.cache.remove_member(team_id, member_id)
            return result
        except NotFound:
            logger.debug(f"Пользователя {member_id} или команды {team_id} не существует")
            raise

    async def exit(self, client_id: ID, team_id: ID):
        logger.debug(f"Попытка выхода пользователя {client_id} из команды {team_id}")
        await self.team_member_repository.remove(team_id, client_id)
        logger.info(f"Пользователь {client_id} вышел из команды {team_id}")
        await self.cache.remove_member(team_id, client_id)
