import os
import yaml
from importlib import resources
from pathlib import Path
from pydantic import BaseModel, Field
# from typing import Dict


class AuthConfig(BaseModel):
    secret_key: str
    algorithm: str
    token_expire_seconds: int = 3600
    root_user: str
    root_password: str


class EnvConfig(BaseModel):
    env: str


class LoggerConfig(BaseModel):
    level: str = "INFO"
    dir: Path = Field(Path(__file__).parent.parent.parent / "logs")


class AppConfig(BaseModel):
    name: str
    root: Path = Field(Path(__file__).parent.parent.parent)
    auth: AuthConfig
    # env: Dict[str, EnvConfig]
    logger: LoggerConfig


class Settings:
    def __init__(self):
        # YAML 파일 로드
        with resources.files("base").joinpath("settings.yaml").open("r", encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)

        self.app = AppConfig(**yaml_data)
        # env = os.getenv("ENV", "local")
        # self.env = self.app.env.get(env)

        self.app.logger.dir.mkdir(parents=True, exist_ok=True)

        if not self.app.auth.secret_key:
            self.app.auth.secret_key = os.urandom(32).hex()


settings = Settings()
