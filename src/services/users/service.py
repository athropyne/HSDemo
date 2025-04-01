from fastapi import Depends
from loguru import logger

from src.core.interfaces import BaseService
from src.core.security import PasswordManager
from src.core.types import ID, IDModel, ReplyMode
from src.services.users.dto.input import CreateAccount, UpdateProfile
from src.services.users.dto.output import UserFullInfo, UserShortInfo
from src.services.users.exc import UserAlreadyExists, UserNotFound
from src.services.users.repository import UserDocumentRepository


class UserService(BaseService):
    def __init__(self,
                 user_repository: UserDocumentRepository = Depends(UserDocumentRepository)):
        self.user_repository = user_repository

    async def create_user(
            self,
            model: CreateAccount,
            output_mode: ReplyMode
    ) -> UserFullInfo | UserShortInfo | IDModel:
        try:
            logger.debug("Попытка регистрации пользователя")
            model.password = PasswordManager.hash(model.password)
            result = await self.user_repository.create_user(model.model_dump(), output_mode)
            logger.info(f"Пользователь {result.id} зарегистрирован")
            return result
        except UserAlreadyExists:
            logger.debug(f"Пользователь {model.login} не зарегистрирован. Логин уже существует")
            raise

    async def update_profile(
            self,
            client_id: ID,
            model: UpdateProfile,
            output_mode: ReplyMode | None
    ):
        try:
            logger.debug(f"Попытка изменения информации профиля пользователя {client_id}")
            result = await self.user_repository.update_profile(client_id,
                                                               model.model_dump(exclude_none=True),
                                                               output_mode)
            logger.info(f"Данные профиля пользователя {client_id} изменены")
            return result
        except UserAlreadyExists:
            logger.debug(f"Данные пользователя {client_id} не изменены. Логин уже существует")
            raise
        except UserNotFound:
            logger.debug(f"Пользователь {client_id} не зарегистрирован в системе.")
            raise

    async def get_by_id(
            self,
            client_id: ID,
            user_id: ID,
            output_mode: ReplyMode
    ):
        try:
            logger.debug(f"Пользователь {client_id} пытается получить профиль {user_id}")
            result = await self.user_repository.get_by_id(user_id, output_mode)
            logger.info(f"Пользователь {client_id} получил профиль {user_id}")
            return result
        except UserNotFound:
            logger.debug(f"Пользователь {user_id} не зарегистрирован в системе.")
            raise

    async def get_list(
            self,
            client_id: int,
            skip: int,
            limit: int,
            output_mode: ReplyMode
    ):
        logger.debug("Попытка получения списка пользователей")
        result: list[UserShortInfo] = await self.user_repository.get_list(skip, limit, output_mode)
        logger.info(f"Пользователь {client_id} пользователей получен")
        return result
