import datetime

from pydantic import Field
from pydantic_core import Url

from src.core.schemas import Case, Team
from src.core.types import IDModel
from src.services.users.dto.output import UserShortInfo


class TeamInfo(IDModel):
    title: str

    @classmethod
    def build_from(cls, team: Team):
        return cls(
            id=team.id,
            title=team.title
        )


class MaterialInfo(IDModel):
    uploader: UserShortInfo
    title: str
    storages_URL: list[Url]
    uploaded_at: datetime.datetime


class CaseFullInfo(IDModel):
    team: TeamInfo = Field(..., description="Команда")
    title: str = Field(..., max_length=100, description="Название случая")
    description: str | None = Field(None, max_length=200, description="Описание случая")
    creator: UserShortInfo = Field(..., description="Создатель")
    created_at: datetime.datetime = Field(..., description="Дата создания")
    materials: list[MaterialInfo]

    class Settings:
        projection = {
            "id": 1,
            "team": {
                "id": "$team._id",
                "title": "$team.title",
            },
            "title": 1,
            "description": 1,
            "creator": {
                "id": "$creator._id",
                "first_name": "$creator.profile.first_name",
                "middle_name": "$creator.profile.middle_name",
                "last_name": "$creator.profile.last_name"
            },
            "created_at": 1,
            "materials": {
                "$map": {
                    "input": "$materials",
                    "as": "material",
                    "in": {
                        "_id": "$$material._id",
                        "uploader": {
                            "id": "$$material.uploader._id",
                            "first_name": "$$material.uploader.first_name",
                            "middle_name": "$$material.uploader.middle_name",
                            "last_name": "$$material.uploader.last_name"
                        },
                        "title": "$$material.title",
                        "uploaded_at": "$$material.uploaded_at"
                    }
                }
            }
        }

    @classmethod
    def build_from(cls, case: Case):
        return cls(
            id=case.id,
            team=TeamInfo.build_from(case.team),
            title=case.title,
            description=case.description,
            creator=UserShortInfo.build_from(case.creator),
            created_at=case.created_at,
            materials=case.materials,
        )


class CaseShortInfo(IDModel):
    title: str = Field(..., max_length=100, description="Название случая")
    description: str | None = Field(None, max_length=200, description="Описание случая")
    created_at: datetime.datetime = Field(..., description="Дата создания")

    class Settings:
        projection = {
            "id": 1,
            "title": 1,
            "description": 1,
            "created_at": 1
        }

    @classmethod
    def build_from(cls, case: Case):
        return cls(
            **case.model_dump()
        )
