from src.core.exc import NotFound


class CaseNotFound(NotFound):
    def __init__(self):
        super().__init__(detail="Случай не найден")