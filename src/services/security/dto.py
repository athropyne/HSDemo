from pydantic import BaseModel, Field


class AuthModel(BaseModel):
    login: str = Field(..., max_length=30)
    password: str = Field(..., max_length=100)


class TokenModel(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    refresh_token: str
