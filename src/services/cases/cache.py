from src.core.infrastructures import RedisStorage
from src.core.types import ID


class CaseCache(RedisStorage):
    async def set_case_admin(self, admin_id: ID, case_id: ID):
        await self.storage.hset(f"case:{case_id}", "admin", str(admin_id))

    async def get_case_admin(self, case_id: ID):
        return await self.storage.hget(f"case:{case_id}", "admin")

    async def set_team_member_for_case(self, user_id: ID, case_id: ID):
        await self.storage.sadd(f"case:{case_id}:members", str(user_id))

    async def is_team_member_in_case(self, user_id: ID, case_id: ID):
        return await self.storage.sismember(f"case:{case_id}:members", str(user_id))

    async def remove_member_from_case(self, user_id: ID, case_id: ID):
        return await self.storage.srem(f"team:{case_id}:members", str(user_id))
