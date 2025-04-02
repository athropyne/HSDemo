from src.core.exc import NotFound, AccessDenied


class CaseNotFound(NotFound):
    def __init__(self):
        super().__init__(detail="Случай не найден")


class CaseAccessDenied(AccessDenied):
    def __init__(self):
        super().__init__(detail="У вас нет доступа к этому случаю")
