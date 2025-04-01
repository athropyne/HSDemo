from src.core.infrastructures import RedisStorage
from src.core.types import ID


class TeamCache(RedisStorage):
    async def set_team_admin(self, admin_id: ID, team_id: ID):
        await self.storage.hset(f"team:{team_id}", "admin", str(admin_id))

    async def add_team_member(self, member_id: ID, team_id: ID):
        await self.storage.sadd(f"team:{team_id}:members", str(member_id))

    async def get_team_admin(self, team_id: ID):
        return await self.storage.hget(f"team:{team_id}", "admin")

    async def is_team_member(self, team_id: ID, member_id: ID):
        return await self.storage.sismember(f"team:{team_id}:members", str(member_id))

    async def remove_member(self, team_id: ID, member_id: ID):
        return await self.storage.srem(f"team:{team_id}:members", str(member_id))

