from typing import Union

from beanie import WriteRules, UpdateResponse
from beanie.odm.operators.find.logical import And
from beanie.odm.operators.update.general import Set
from pymongo.results import UpdateResult

from src.core.schemas import Team
from src.core.types import ID, IDModel, ReplyMode
from src.services.teams.dto.output import TeamFullInfo, TeamShortInfo
from src.services.teams.exc import TeamNotFound
from src.services.users.dto.output import UserShortInfo
from src.services.users.repository import UserDocumentRepository


class TeamRepository:
    async def create(self,
                     client_id: ID,
                     data: dict,
                     output_mode: ReplyMode) -> Union[TeamFullInfo, TeamShortInfo, IDModel]:
        user = await UserDocumentRepository.get_document_by_id(client_id)
        team = Team(
            **data,
            creator=client_id,
            administrator=client_id,
            members=[client_id]
        )
        result: Team = await team.insert(link_rule=WriteRules.WRITE)
        result.creator, result.administrator, result.members = user, user, [UserShortInfo.build_from(user)]
        projection_model = ReplyMode.build_reply(output_mode, TeamFullInfo, TeamShortInfo)

        return projection_model.build_from(result)

    def __build_query_projection(self, query, output_mode: ReplyMode):
        match output_mode:
            case ReplyMode.FULL:
                return query.project(TeamFullInfo)
            case ReplyMode.SHORT:
                return query.project(TeamShortInfo)
            case ReplyMode.ID:
                return query.project(IDModel)

    async def get_by_id(self, team_id: ID, output_mode: ReplyMode) -> Union[TeamFullInfo, TeamShortInfo, IDModel]:
        query = Team.find_one(Team.id == team_id, fetch_links=True)
        result = await self.__build_query_projection(query, output_mode)
        if not result:
            raise TeamNotFound
        return result

    async def get_list(self, client_id: ID, skip: int, limit: int, output_mode: ReplyMode):
        query = Team.find(Team.members.id == client_id, fetch_links=True).skip(skip).limit(limit)
        return await self.__build_query_projection(query, output_mode).to_list()

    async def update(self, team_id: ID, data: dict, output_mode: ReplyMode):
        result: UpdateResult = await Team.find_one(Team.id == team_id).update(Set(data),
                                                                              response_type=UpdateResponse.UPDATE_RESULT)
        if result.matched_count == 0:
            raise TeamNotFound
        if output_mode is ReplyMode.ID:
            return IDModel(id=team_id)
        return await self.get_by_id(team_id, output_mode)

    async def delete(self, team_id: ID):
        team = await self.get_document_by_id(team_id)
        result = await team.delete()
        if result.deleted_count == 0:
            raise TeamNotFound

    async def is_team_member(self, team_id: ID, user_id: ID):
        return await Team.find_one(And(Team.id == team_id, Team.members.id == user_id)).project(IDModel).exists()

    @staticmethod
    async def get_document_by_id(team_id: ID):
        team = await Team.get(team_id)
        if team is None:
            raise TeamNotFound
        return team
