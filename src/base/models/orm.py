import pickle

from fastapi.encoders import jsonable_encoder
from sqlalchemy import BOOLEAN, CHAR, JSON, Column, Integer, PickleType, String, Text
from sqlalchemy.orm import DeclarativeBase
from typing import Optional

from ..config import ENV
from .exception import Fallback


class Base(DeclarativeBase):
    pass


class UserORM(Base):
    __tablename__ = "tb_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(CHAR(30), nullable=False, unique=True)
    password = Column(CHAR(255), nullable=False)
    disabled = Column(BOOLEAN(), nullable=False)

    def __init__(self, username: str, password: str, disable: bool = False):
        self.username = username
        self.password = password
        self.disabled = disable
        super().__init__()

    def __repr__(self):
        return f"<User({self.id}, {self.username}, {self.disabled})>"

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "disabled": self.disabled,
        }


class FallbackORM(Base):
    __tablename__ = "tb_fallback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(40), nullable=False)
    traceback = Column(Text, nullable=True)
    env = Column(JSON, nullable=True)
    data = Column(PickleType, nullable=True)

    def __init__(self, fallback: Fallback, data: Optional[object] = None):
        self.type = fallback.type
        self.traceback = fallback.traceback
        self.env = jsonable_encoder(ENV.dict(exclude=ENV.except_vars()))
        self.data = pickle.dumps(data) if data else None
        super().__init__()

    def __repr__(self):
        return f"<Fallback({self.id}, {self.type}, {self.traceback})>"

    def as_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "traceback": self.traceback,
            "env": self.env,
            "data": pickle.loads(self.data).dict() if self.data else None,
        }
