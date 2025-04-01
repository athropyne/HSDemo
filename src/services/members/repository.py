from typing import Literal

from beanie import UpdateResponse
from beanie.odm.operators.update.array import AddToSet, Pull
from bson import DBRef
from pymongo.results import UpdateResult

from src.core.schemas import Team, User
from src.core.types import ID
from src.services.members.exc import TeamMemberAlreadyExists
from src.services.teams.exc import TeamNotFound
from src.services.users.exc import UserNotFound


class TeamMemberRepository:
    def __get_query(self, team_id: ID, user: User, action: Literal["add", "remove"]):
        return Team.find_one(Team.id == team_id).update(
            AddToSet(
                {Team.members: DBRef(User.Settings.name, user.id)}
            ) if action == "add" else Pull(
                {Team.members: DBRef(User.Settings.name, user.id)}
            ),
            response_type=UpdateResponse.UPDATE_RESULT
        )

    async def __update(self, team_id: ID, member_id: ID, action: Literal["add", "remove"]) -> UpdateResult:
        user = await User.get(member_id)
        if not user:
            raise UserNotFound

        result: UpdateResult = await self.__get_query(team_id, user, action)
        if result.matched_count == 0:
            raise TeamNotFound
        return result

    async def add(self, team_id: ID, member_id: ID):
        result = await self.__update(team_id, member_id, "add")
        if result.modified_count == 0:
            raise TeamMemberAlreadyExists

    async def remove(self, team_id: ID, member_id: ID):
        result = await self.__update(team_id, member_id, "remove")
        if result.modified_count == 0:
            raise UserNotFound

