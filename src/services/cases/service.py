from fastapi import Depends
from loguru import logger
from psycopg.errors import CaseNotFound

from src.core.interfaces import BaseService
from src.core.types import ID, ReplyMode, IDModel
from src.services.cases.dto.input import CreateCase, UpdateCase
from src.services.cases.dto.output import CaseFullInfo, CaseShortInfo
from src.services.cases.repository import CaseRepository


class CaseService(BaseService):
    def __init__(self,
                 case_repository: CaseRepository = Depends(CaseRepository)):
        self.case_repository = case_repository

    async def create(
            self,
            client_id: ID,
            model: CreateCase,
            output_mode: ReplyMode
    ) -> CaseFullInfo | CaseShortInfo | IDModel:
        logger.debug(f"Пользователь {client_id} пытается создать случай в команде {model.team_id}")
        case = await self.case_repository.create(client_id, model, output_mode)
        logger.info(f"Пользователь {client_id} создал случай {case.id}")
        return case

    async def update(
            self,
            client_id: ID,
            case_id: ID,
            model: UpdateCase,
            output_mode: ReplyMode
    ) -> CaseFullInfo | CaseShortInfo | IDModel:
        try:
            logger.debug(f"Пользователь {client_id} пытается изменить случай {case_id}")
            case = await self.case_repository.update(case_id, model.model_dump(exclude_none=True), output_mode)
            logger.info(f"Пользователь {client_id} получил информацию о случае {case_id}")
            return case
        except CaseNotFound:
            logger.debug(f"Случай {case_id} не найден")
            raise

    async def get_by_id(
            self,
            client_id: ID,
            case_id: ID,
            output_mode: ReplyMode
    ) -> CaseFullInfo | CaseShortInfo | IDModel:
        logger.debug(f"Пользователь {client_id} пытается получить случай {case_id}")
        result = await self.case_repository.get_by_id(case_id, output_mode)
        logger.info(f"Пользователь {client_id} получил информацию о случае {case_id}")
        return result

    async def get_list(
            self,
            client_id: ID,
            team_id: ID,
            skip: int,
            limit: int,
            output_mode: ReplyMode
    ) -> list[CaseFullInfo | CaseShortInfo | IDModel]:
        logger.debug(f"Пользователь {client_id} пытается получить список случаев команды {team_id}")
        result = await self.case_repository.get_list(team_id, skip, limit, output_mode)
        logger.info(f"Пользователь {client_id} получил список случаев команды {team_id}")
        return result

    async def delete(self,
                     client_id: ID,
                     case_id: ID):
        logger.debug(f"Пользователь {client_id} пытается удалить случай {case_id}")
        await self.case_repository.delete(case_id)
        logger.info(f"Пользователь {client_id} удалил случай {case_id}")
