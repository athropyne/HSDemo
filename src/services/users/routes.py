from typing import Union

from fastapi import APIRouter, Depends, Query
from starlette import status

from src.core.security import TokenManager
from src.core.types import ID, IDModel, ReplyMode
from src.services.users.dto.input import CreateAccount, UpdateProfile
from src.services.users.dto.output import UserFullInfo, UserShortInfo
from src.services.users.service import UserService

user_router = APIRouter(prefix="/users", tags=["Пользователи"])


@user_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового пользователя",
    description="""Создает новый аккаунт и пустой профиль. 
    Возвращает данные профиля с логином, 
    только ID пользователя
    или None в зависимости от опции output_mode""",
    response_model=Union[UserFullInfo, UserShortInfo, IDModel]
)
async def create_user(
        model: CreateAccount,
        output_mode: ReplyMode | None = Query(ReplyMode.ID, description="режим возврата данных"),
        service: UserService = Depends(UserService)
):
    return await service.create_user(model, output_mode)


@user_router.put(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Изменить данные своего профиля",
    description="""Обновляет данные профиля клиента. Возвращает новые данные профиля.
    В этой версии API только сам пользователь может изменить свои данные.
    Возвращает данные профиля с логином, 
    только ID пользователя
    или None в зависимости от опции output_mode""",
    response_model=Union[UserFullInfo, UserShortInfo, IDModel]
)
async def update_profile(
        model: UpdateProfile,
        output_mode: ReplyMode | None = Query(ReplyMode.ID, description="режим возврата данных"),
        client_id: ID = Depends(TokenManager.decode),
        service: UserService = Depends(UserService)
):
    return await service.update_profile(client_id, model, output_mode)


@user_router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Получить данные профиля по ID",
    description="""Возвращает данные профиля пользователя по идентификатору. 
    Запросить данные может любой пользователь""",
    response_model=Union[UserFullInfo, UserShortInfo, IDModel]
)
async def get_by_id(
        user_id: ID,
        output_mode: ReplyMode = ReplyMode.FULL,
        client_id: ID = Depends(TokenManager.decode),
        service: UserService = Depends(UserService)
):
    return await service.get_by_id(client_id, user_id, output_mode)


@user_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Получить список пользователей",
    description="""Возвращает список профилей. В этой версии API возвращается полная информация о профилях.""",
    response_model=list[Union[UserFullInfo, UserShortInfo, IDModel]]
)
async def get_list(
        output_mode: ReplyMode = ReplyMode.SHORT,
        skip: int = 0,
        limit: int = 30,
        client_id: int = Depends(TokenManager.decode),
        service: UserService = Depends(UserService)
):
    return await service.get_list(client_id, skip, limit, output_mode)
