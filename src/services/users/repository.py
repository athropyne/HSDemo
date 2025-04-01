from typing import Union

from pymongo.errors import DuplicateKeyError

from src.core.schemas import User, Account, Profile
from src.core.types import ID, ReplyMode, IDModel
from src.services.users.dto.output import UserShortInfo, UserFullInfo
from src.services.users.exc import UserAlreadyExists, UserNotFound


class UserDocumentRepository:
    async def create_user(self, data: dict, output_mode: ReplyMode) -> UserFullInfo | UserShortInfo | IDModel | None:
        try:
            user = await User(account=Account(**data), profile=Profile()).insert()
            projection_model = ReplyMode.build_reply(output_mode, UserFullInfo, UserShortInfo)
            return projection_model.build_from(user)
        except DuplicateKeyError:
            raise UserAlreadyExists

    async def update_profile(self, client_id: ID, data: dict, output_mode: ReplyMode):
        try:
            user = await User.get(client_id)
            if user is None:
                raise UserNotFound
            user.profile = Profile(**data)
            result = await user.save()
            projection_model = ReplyMode.build_reply(output_mode, UserFullInfo, UserShortInfo)
            return projection_model.build_from(result)
        except DuplicateKeyError:
            raise UserAlreadyExists

    async def get_list(self,
                       skip: int,
                       limit: int,
                       output_mode: ReplyMode) -> list[Union[UserFullInfo, UserShortInfo, IDModel]]:
        projection_model = ReplyMode.build_reply(output_mode, UserFullInfo, UserShortInfo)
        return await User.find({}, projection_model=projection_model).skip(skip).limit(limit).to_list()

    async def get_by_id(self, user_id: ID, output_mode: ReplyMode):
        projection_model = ReplyMode.build_reply(output_mode, UserFullInfo, UserShortInfo)
        user = await User.find_one(User.id == user_id, projection_model=projection_model)
        if user is None:
            raise UserNotFound
        return user

    @staticmethod
    async def get_document_by_id(user_id: ID):
        user = await User.get(user_id)
        if user is None:
            raise UserNotFound
        return user
