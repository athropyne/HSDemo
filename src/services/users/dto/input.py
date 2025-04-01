from pydantic import BaseModel, Field

from src.core.types import DTO


class CreateAccount(DTO):
    login: str = Field(..., max_length=30)
    password: str = Field(...)


class UpdateProfile(BaseModel):
    first_name: str | None = Field(None, max_length=50, description="Имя")
    middle_name: str | None = Field(None, max_length=50, description="Отчество")
    last_name: str | None = Field(None, max_length=50, description="Фамилия")
