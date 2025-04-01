from pydantic import BaseModel, Field
from pydantic_core import Url


class StorageAddInputModel(BaseModel):
    storage_URL: Url = Field(..., description="Адрес внешнего хранилища слайдов")
