from uuid import UUID

from sqlalchemy import CursorResult, select

from src.core.interfaces import BaseRepository
# from src.core.schemas import materials
from src.services.materials.exc import MaterialNotFound


class MaterialRepository(BaseRepository):
    async def create(self, data: dict):
        async with self.engine.connect() as connection:
            cursor: CursorResult = await connection.execute(
                materials
                .insert()
                .values(data)
                .returning(materials.c.material_id)
            )
            await connection.commit()
        return cursor.scalar()

    async def update(self, material_id: UUID, data: dict):
        async with self.engine.connect() as connection:
            cursor: CursorResult = await connection.execute(
                materials
                .values(data)
                .where(materials.c.material_id == material_id)
            )
            if cursor.rowcount != 1:
                raise MaterialNotFound
            await connection.commit()

    async def get_list(self, case_id: int):
        async with self.engine.connect() as connection:
            cursor: CursorResult = await connection.execute(
                select(materials)
                .where(materials.c.case_id == case_id)
            )
        return cursor.mappings().fetchall()

    # async def get_by_id(self, material_id: int): ...

    async def delete(self, material_id: UUID):
        async with self.engine.connect() as connection:
            cursor: CursorResult = await connection.execute(
                materials
                .delete()
                .where(materials.c.material_id == material_id)
            )
