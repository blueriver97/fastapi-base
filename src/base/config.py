import os
from datetime import datetime
from typing import Any
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Note. System Settings
    app_name: str = Field("", alias="BASE_APP_NAME")
    base_dir: str = Field(os.path.dirname(os.path.abspath(__file__)))  # base

    # Note. Logger Settings
    log_dir: str = Field(f"{os.path.expanduser('~')}/logs")
    log_file: str = Field(f"{datetime.now().strftime('%Y%m%d')}.log")
    log_level: int = Field(10)  # DEBUG=10, INFO=20

    # Note. Auth Secret Key
    auth_secret_key: str = Field(None, alias="AUTH_SECRET_KEY")

    @field_validator("auth_secret_key")
    @classmethod
    def ensure_foobar(cls, v: Any):
        if not v:
            raise ValueError("auth_secret_key cannot be empty or None")
        return v

    def except_vars(self):
        return []

    """
    #################################
    # 사용자 변수 설정은 아래에 작성 할 것 #
    #################################
    """


ENV = Settings()
ENV.log_file = f"{ENV.app_name}-{ENV.log_file}"
