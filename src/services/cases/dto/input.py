from pydantic import BaseModel, Field

from src.core.types import ID


class CreateCase(BaseModel):
    team_id: ID = Field(..., description="Идентификатор команды")
    title: str = Field(..., max_length=100, description="Название случая")
    description: str | None = Field(None, max_length=1000, description="Описание случая")


class UpdateCase(BaseModel):
    title: str | None = Field(None, max_length=100, description="Название случая")
    description: str | None = Field(None, max_length=1000, description="Описание случая")