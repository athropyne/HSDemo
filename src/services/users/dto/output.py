import datetime

from pydantic import Field

from src.core.schemas import User
from src.core.types import IDModel, OutputModel


class UserFullInfo(IDModel):
    login: str = Field(description="Логин")
    first_name: str | None = Field(description="Имя")
    middle_name: str | None = Field(description="Отчество")
    last_name: str | None = Field(description="Фамилия")
    created_at: datetime.datetime = Field(description="Дата регистрации")

    class Settings:
        projection = {
            "id": 1,
            "login": "$account.login",
            "first_name": "$profile.first_name",
            "middle_name": "$profile.middle_name",
            "last_name": "$profile.last_name",
            "created_at": 1
        }

    @classmethod
    def build_from(cls, user: User):
        return cls(
            id=user.id,
            login=user.account.login,
            first_name=user.profile.first_name,
            middle_name=user.profile.middle_name,
            last_name=user.profile.last_name,
            created_at=user.created_at
        )


class UserShortInfo(IDModel):
    first_name: str | None
    middle_name: str | None
    last_name: str | None

    class Settings:
        projection = {
            "_id": 1,
            "first_name": "$profile.first_name",
            "middle_name": "$profile.middle_name",
            "last_name": "$profile.last_name",
        }

    @classmethod
    def build_from(cls,
                   user: User):
        return cls(
            id=user.id,
            first_name=user.profile.first_name,
            middle_name=user.profile.middle_name,
            last_name=user.profile.last_name
        )
