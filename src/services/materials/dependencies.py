from fastapi import Depends

from src.core.security import TokenManager
from src.services.materials.dto import MaterialAddInputModel


def build_create_model(
        case_id: int,
        title: str,
        client_id: int = Depends(TokenManager.decode),
):
    return MaterialAddInputModel(
        case_id=case_id,
        title=title,
        uploader_id=client_id
    )
