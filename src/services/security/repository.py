from src.core.schemas import User


class SecurityRepository:
    async def find_by_login(self, login: str) -> User:
        user = await User.find_one(User.account.login == login)
        return user
