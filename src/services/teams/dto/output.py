import datetime

from pydantic import Field

from src.core.schemas import Team
from src.core.types import IDModel
from src.services.users.dto.output import UserShortInfo


class TeamFullInfo(IDModel):
    title: str = Field(description="Название команды")
    creator: UserShortInfo
    administrator: UserShortInfo
    members: list[UserShortInfo]
    created_at: datetime.datetime = Field(..., description="Дата и время создания команды")

    class Settings:
        projection = {
            "_id": 1,
            "title": 1,
            "creator": {
                "_id": "$creator._id",
                "first_name": "$creator.profile.first_name",
                "middle_name": "$creator.profile.middle_name",
                "last_name": "$creator.profile.last_name"
            },
            "administrator": {
                "_id": "$administrator._id",
                "first_name": "$administrator.profile.first_name",
                "middle_name": "$administrator.profile.middle_name",
                "last_name": "$administrator.profile.last_name"
            },
            "members": {
                "$map": {
                    "input": "$members",
                    "as": "member",
                    "in": {
                        "_id": "$$member._id",
                        "first_name": "$$member.profile.first_name",
                        "middle_name": "$$member.profile.middle_name",
                        "last_name": "$$member.profile.last_name"
                    }
                }
            },
            "created_at": 1
        }

    @classmethod
    def build_from(cls, team: Team):
        return cls(
            id=team.id,
            title=team.title,
            creator=UserShortInfo.build_from(team.creator),
            administrator=UserShortInfo.build_from(team.administrator),
            members=team.members,
            created_at=team.created_at,
        )


class TeamShortInfo(IDModel):
    title: str = Field(..., max_length=100, description="Название команды")
    administrator: UserShortInfo = Field(..., description="Администратор")
    created_at: datetime.datetime = Field(..., description="Дата и время создания команды")

    class Settings:
        projection = {
            "_id": 1,
            "title": 1,
            "administrator": {
                "id": "$administrator._id",
                "first_name": "$administrator.profile.first_name",
                "middle_name": "$administrator.profile.middle_name",
                "last_name": "$administrator.profile.last_name"
            },
            "created_at": 1
        }

    @classmethod
    def build_from(cls, team: Team):
        return cls(
            id=team.id,
            title=team.title,
            administrator=UserShortInfo.build_from(team.administrator),
            created_at=team.created_at,
        )
