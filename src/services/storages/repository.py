from sqlalchemy import CursorResult, select

from src.core.interfaces import BaseRepository
# from src.core.schemas import storages


# class StorageRepository(BaseRepository):
#     async def add(self, data: dict):
#         async with self.engine.connect() as connection:
#             cursor: CursorResult = await connection.execute(
#                 storages
#                 .insert()
#                 .values(data)
#                 .returning(storages)
#             )
#         return cursor.scalar()

    # async def get_list(self):
    #     async with self.engine.connect() as connection:
    #         cursor: CursorResult = await connection.execute(
    #             select(storages)
    #         )
    #     return cursor.mappings().fetchall()
    #
    # async def delete(self, storage_URL: str):
    #     async with self.engine.connect() as connection:
    #         cursor: CursorResult = await connection.execute(
    #             storages
    #             .delete()
    #             .where(storages.c.storage_URL == storage_URL)
    #         )
