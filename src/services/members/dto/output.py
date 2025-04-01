from src.core.schemas import Team
from src.core.types import OutputModel
from src.services.users.dto.output import UserShortInfo


class MembersFullInfo(OutputModel):
    members: list[UserShortInfo]

    @classmethod
    def build_from(cls, team: Team):
        return cls(
            members=team.members
        )


