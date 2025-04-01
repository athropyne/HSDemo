from pydantic import BaseModel, Field


class MaterialAddInputModel(BaseModel):
    case_id: int = Field(..., description="Идентификатор случая")
    uploader_id: int = Field(..., description="Идентификатор создателя материала")
    title: str = Field(..., max_length=100, description="Название")


class MaterialUpdateInputModel(BaseModel):
    title: str | None = Field(None, max_length=100, description="Название")
