from fastapi import Depends

from src.core.dependencies import D
from src.core.infrastructures import Database
from src.core.utils import catch
from sqlalchemy.ext.asyncio import AsyncEngine


class BaseService:
    pass


class BaseRepository:
    def __init__(self,
                 database: Database = Depends(D.database)):
        self.engine: AsyncEngine = database.engine

    def __getattribute__(self, item):
        attr = super().__getattribute__(item)
        if callable(attr):
            @catch
            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                return result

            return wrapper

        return attr

