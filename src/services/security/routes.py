from fastapi import APIRouter, Depends

from src.core import utils
from src.services.security.dto import TokenModel, AuthModel
from src.services.security.service import SecurityService

security_router = APIRouter(prefix="/security", tags=["Безопасность"])


@security_router.post("/",
                      response_model=TokenModel)
async def auth(
        model: AuthModel = Depends(utils.convert_auth_data),
        service: SecurityService = Depends(SecurityService)
):
    return await service.auth(model)
