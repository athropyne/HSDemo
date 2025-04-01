from src.core.exc import NotFound


class MaterialNotFound(NotFound):
    def __init__(self):
        super().__init__(detail="Материал не найден")