from functools import wraps
from typing import Callable

import sqlalchemy
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from starlette import status

from src.services.security.dto import AuthModel


def catch(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except sqlalchemy.exc.OperationalError:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                                detail="outside service is not available")
        except:
            raise

    return wrapper


def convert_auth_data(data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    return AuthModel(login=data.username, password=data.password)
