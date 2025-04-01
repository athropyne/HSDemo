from abc import ABC, abstractmethod
from enum import Enum
from typing import Type

from beanie import PydanticObjectId, Document
from pydantic import BaseModel, Field, ConfigDict

ID = PydanticObjectId


class DTO(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ID: str},
        populate_by_name=True,
    )


class OutputModel(DTO, ABC):
    @classmethod
    @abstractmethod
    def build_from(cls, document: Document): ...


class IDModel(OutputModel):
    id: ID = Field(alias="_id", serialization_alias="id")

    @classmethod
    def build_from(cls, document: Document):
        return cls(id=document.id)


class ReplyMode(Enum):
    FULL = "full"
    SHORT = "short"
    ID = "only id"

    def build_reply(self,
                    full_model: Type[BaseModel],
                    short_model: Type[BaseModel]):
        match self:
            case self.FULL:
                return full_model
            case self.SHORT:
                return short_model
            case self.ID:
                return IDModel
