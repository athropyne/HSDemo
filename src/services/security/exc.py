from fastapi import HTTPException
from starlette import status


class InvalidLoginOrPassword(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Неверный логин или пароль")


