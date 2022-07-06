from typing import Optional
from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str
    keep_login: bool = False


class TokenBase(BaseModel):
    access_token: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UserToken(TokenBase):
    refresh_token: str
    token_type: str
