from fastapi import Depends

from src.core.interfaces import BaseService
from src.core.security import PasswordManager, TokenManager, TokenTypes
from src.services.security.dto import AuthModel, TokenModel
from src.services.security.exc import InvalidLoginOrPassword
from src.services.security.repository import SecurityRepository


class SecurityService(BaseService):
    def __init__(self,
                 repository: SecurityRepository = Depends(SecurityRepository)):
        self.repository = repository

    async def auth(self, model: AuthModel):
        result = await self.repository.find_by_login(model.login)
        if result is not None:
            if PasswordManager.verify(model.password, result.account.password):
                access_token = TokenManager.create({"id": str(result.id)}, TokenTypes.ACCESS)
                refresh_token = TokenManager.create({"id": str(result.id)}, TokenTypes.REFRESH)
                return TokenModel(
                    access_token=access_token,
                    refresh_token=refresh_token
                )
        raise InvalidLoginOrPassword

