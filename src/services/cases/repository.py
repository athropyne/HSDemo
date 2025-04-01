from beanie import WriteRules, UpdateResponse
from beanie.odm.operators.update.general import Set
from pymongo.results import UpdateResult, DeleteResult

from src.core.schemas import Case
from src.core.types import ID, ReplyMode, IDModel
from src.services.cases.dto.input import CreateCase
from src.services.cases.dto.output import CaseFullInfo, CaseShortInfo
from src.services.cases.exc import CaseNotFound
from src.services.teams.repository import TeamRepository
from src.services.users.repository import UserDocumentRepository


class CaseRepository:
    async def create(
            self,
            client_id: ID,
            model: CreateCase,
            output_mode: ReplyMode
    ) -> CaseFullInfo | CaseShortInfo | IDModel:
        user = await UserDocumentRepository.get_document_by_id(client_id)
        team = await TeamRepository.get_document_by_id(model.team_id)
        case = Case(
            team=team,
            creator=user,
            title=model.title,
            description=model.description,
            materials=[]
        )
        result: Case = await case.save(link_rule=WriteRules.WRITE)
        result.creator = user
        projection_model = ReplyMode.build_reply(output_mode, CaseFullInfo, CaseShortInfo)
        return projection_model.build_from(result)

    async def get_by_id(self, case_id: ID, output_mode: ReplyMode) -> CaseFullInfo | CaseShortInfo | IDModel:
        query = Case.find_one(Case.id == case_id, fetch_links=True if output_mode is ReplyMode.FULL else False)
        case = ...
        match output_mode:
            case ReplyMode.FULL:
                case = await query.project(CaseFullInfo)
            case ReplyMode.SHORT:
                case = await query.project(CaseShortInfo)
            case ReplyMode.ID:
                case = await query.project(IDModel)
        if case is None:
            raise CaseNotFound
        return case

    async def update(
            self, case_id: ID,
            data: dict,
            output_mode: ReplyMode
    ) -> CaseFullInfo | CaseShortInfo | IDModel:
        result: UpdateResult = await Case.find_one(Case.id == case_id).update(Set(data),
                                                                              response_type=UpdateResponse.UPDATE_RESULT)
        if result.matched_count == 0:
            raise CaseNotFound
        if output_mode is ReplyMode.ID:
            return IDModel(id=case_id)
        return await self.get_by_id(case_id, output_mode)

    async def get_list(
            self,
            team_id: ID,
            skip: int | None,
            limit: int | None,
            output_mode: ReplyMode
    ) -> list[CaseFullInfo | CaseShortInfo | IDModel]:
        query = Case.find(Case.team.id == team_id, fetch_links=True).skip(skip).limit(limit)
        match output_mode:
            case ReplyMode.FULL:
                return await query.project(CaseFullInfo).to_list()
            case ReplyMode.SHORT:
                return await query.project(CaseShortInfo).to_list()
            case ReplyMode.ID:
                return await query.project(IDModel).to_list()

    async def delete(self, case_id: ID):
        result: DeleteResult = await Case.find_one(Case.id == case_id).delete()
        if result.deleted_count == 0:
            raise CaseNotFound

    @staticmethod
    async def get_document_by_id(case_id: ID):
        case = Case.get(case_id)
        if case is None:
            raise CaseNotFound
        return case

    @staticmethod
    async def delete_cases_in_team(team_id: ID):
        await Case.find(Case.team.id == team_id).delete()
