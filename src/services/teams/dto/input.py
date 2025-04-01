from pydantic import BaseModel, Field


class CreateTeam(BaseModel):
    title: str = Field(..., max_length=100, description="Название команды")


class UpdateTeam(BaseModel):
    title: str = Field(..., max_length=100, description="Название команды")
