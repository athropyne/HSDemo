import datetime

import pymongo
from beanie import Document, Link, BackLink, before_event, Delete
from loguru import logger
from pydantic import Field, BaseModel
from pydantic_core import Url
from pymongo import IndexModel


class Account(BaseModel):
    login: str = Field(..., max_length=30)
    password: str = Field(...)


class Profile(BaseModel):
    first_name: str | None = Field(None, max_length=50)
    middle_name: str | None = Field(None, max_length=50)
    last_name: str | None = Field(None, max_length=50)


class User(Document):
    account: Account = Field(...)
    profile: Profile = Field(...)
    created_at: datetime.datetime = Field(..., default_factory=datetime.datetime.now)

    class Settings:
        name = "users"
        use_state_management = True
        indexes = [
            IndexModel(
                [("account.login", pymongo.ASCENDING)],
                name="login_index_ASCENDING",
                unique=True
            ),
        ]


class Team(Document):
    title: str = Field(..., max_length=100)
    creator: Link[User]
    administrator: Link[User]
    created_at: datetime.datetime = Field(..., default_factory=datetime.datetime.now)
    members: list[Link[User]] = Field(..., max_length=100, default_factory=list)
    case: list[BackLink["Case"]] = Field(original_field="team")

    @before_event(Delete)
    async def delete_cases(self):
        logger.debug(f"Попытка удаления всех случаев в команде f{self.id}")
        result = await Case.find(Case.team.id == self.id).delete()
        logger.info(f"В команде {self.id} случаев удалено: {result.deleted_count}.")

    class Settings:
        name = "teams"
        use_state_management = True


class Material(Document):
    uploader: Link[User]
    title: str = Field(..., max_length=100)
    storages_URL: list[Url]
    uploaded_at: datetime.datetime = Field(..., default_factory=datetime.datetime.now)

    class Settings:
        name = "materials"


class Case(Document):
    team: Link[Team]
    creator: Link[User]
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=2000)
    materials: list[Material]
    created_at: datetime.datetime = Field(..., default_factory=datetime.datetime.now)

    @before_event(Delete)
    async def clear_materials(self):
        # write here !!!
        ...

    class Settings:
        name = "cases"


class Storage(Document):
    storage_URL: Url
