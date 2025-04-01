from src.core.exc import AlreadyExists, NotFound


class UserAlreadyExists(AlreadyExists):
    def __init__(self):
        super().__init__(detail="Пользователь с таким логином уже существует")


class UserNotFound(NotFound):
    def __init__(self):
        super().__init__(detail="Пользователь не найден")
