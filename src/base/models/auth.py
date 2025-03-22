from typing import Optional

from fastapi.param_functions import Form
from pydantic import BaseModel, SecretStr


class User(BaseModel):
    id: int
    username: str
    password: str
    disabled: bool

    class Config:
        from_attribute = True


class UserOutput(BaseModel):
    id: int
    username: str
    disabled: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class CustomOAuth2PasswordRequestForm:
    def __init__(
        self,
        grant_type: str = Form(default=None, regex="password"),
        username: str = Form(),
        password: SecretStr = Form(),
        scope: str = Form(default=""),
        client_id: Optional[str] = Form(default=None),
        client_secret: Optional[str] = Form(default=None),
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
