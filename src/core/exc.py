from fastapi import HTTPException
from starlette import status


class AlreadyExists(HTTPException):
    def __init__(self,
                 detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=detail)


class NotFound(HTTPException):
    def __init__(self,
                 detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail=detail)


class InvalidData(AlreadyExists):
    ...


class AccessDenied(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN,
                         detail=detail)
