from fastapi import Depends
from loguru import logger

from src.core.interfaces import BaseService
from src.core.types import ID, ReplyMode
from src.services.teams.cache import TeamCache
from src.services.teams.dto.input import CreateTeam, UpdateTeam
from src.services.teams.exc import EmptyPayloadError, TeamNotFound, TeamAlreadyExistsError
from src.services.teams.repository import TeamRepository


class TeamService(BaseService):
    def __init__(self,
                 team_repository: TeamRepository = Depends(TeamRepository),
                 team_cache: TeamCache = Depends(TeamCache)):
        self.team_repository = team_repository
        self.team_cache = team_cache

    async def create(self,
                     client_id: ID,
                     model: CreateTeam,
                     output_mode: ReplyMode):
        try:
            logger.debug(f"Попытка пользователя {client_id} создать команду")
            result = await self.team_repository.create(client_id, model.model_dump(), output_mode)
            logger.info(f"Пользователь {client_id} создал команду {result.id}")
            await self.team_cache.set_team_admin(client_id, result.id)
            logger.debug(f"Администратор {client_id} команды {result.id} добавлен в кэш.")
            await self.team_cache.add_team_member(client_id, result.id)
            logger.debug(f"Участник {client_id} команды {result.id} добавлен в кэш.")
            return result
        except TeamAlreadyExistsError:
            logger.debug(f"Команда с названием {model.title} уже существует")
            raise

    async def update(self,
                     client_id: ID,
                     team_id: ID,
                     model: UpdateTeam,
                     output_mode: ReplyMode):
        try:
            logger.debug(f"Попытка пользователя {client_id} изменить команду {team_id}")
            data = model.model_dump(exclude_none=True)
            if len(data) == 0:
                raise EmptyPayloadError
            result = await self.team_repository.update(team_id, model.model_dump(exclude_none=True), output_mode)
            logger.info(f"Пользователь {client_id} изменил команду {team_id}")
            return result
        except TeamNotFound:
            logger.debug(f"Команды с идентификатором {team_id} не существует")
            raise

    async def get_by_id(self,
                        client_id: int,
                        team_id: ID,
                        output_mode: ReplyMode):
        try:
            logger.debug(f"Попытка пользователя {client_id} получить данные команды {team_id}")
            result = await self.team_repository.get_by_id(team_id, output_mode)
            logger.debug(f"Пользователь {client_id} получил данные команды {team_id}")
            return result
        except TeamNotFound:
            logger.debug(f"Команды с идентификатором {team_id} не существует")
            raise

    async def get_list(self,
                       client_id: ID,
                       skip: int,
                       limit: int,
                       output_mode: ReplyMode):
        logger.debug(f"Пользователь {client_id} пытается получить список команд")
        result = await self.team_repository.get_list(client_id, skip, limit, output_mode)
        logger.info(f"Пользователь {client_id} получил список команд")
        return result

    async def delete(self,
                     client_id: ID,
                     team_id: ID):
        try:
            logger.debug(f"Пользователь {client_id} пытается удалить команду {team_id}")
            await self.team_repository.delete(team_id)
            logger.info(f"Пользователь {client_id} удалил команду {team_id}")
        except TeamNotFound:
            logger.debug(f"Команды с идентификатором {team_id} не существует")
            raise
