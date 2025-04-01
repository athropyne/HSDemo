from src.core.exc import InvalidData, NotFound, AlreadyExists, AccessDenied


class EmptyPayloadError(InvalidData):
    def __init__(self):
        super().__init__(detail="Нет данных для обновления")


class TeamNotFound(NotFound):
    def __init__(self):
        super().__init__(detail=f"Команды с таким идентификатором не существует")


class TeamAlreadyExistsError(AlreadyExists):
    def __init__(self):
        super().__init__(detail="Команда с таким названием уже существует")


class YouNotAdministrator(AccessDenied):
    def __init__(self):
        super().__init__(detail="Вы не являетесь администратором команды")


class YouNotTeamMember(AccessDenied):
    def __init__(self):
        super().__init__(detail="Вы не являетесь участником команды")


class DeleteAdministratorError(InvalidData):
    def __init__(self):
        super().__init__(detail="Вы не можете удалить самого себя из команды")
