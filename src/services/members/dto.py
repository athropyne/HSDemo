from pydantic import BaseModel, Field

# from src.services.teams.dto import TeamMemberRoles


class TeamMemberAddInputModel(BaseModel):
    member_id: int = Field(..., description="Идентификатор пользователя")


class TeamMemberAddContainer(TeamMemberAddInputModel):
    team_id: int = Field(..., description="Идентификатор команды")


class TeamMemberCreatedOutputModel(BaseModel):
    team_id: int = Field(..., description="Идентификатор команды")
    member_id: int = Field(..., description="Идентификатор участника")
    # member_role: TeamMemberRoles = Field(..., description="Роль участника команды")
