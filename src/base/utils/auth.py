import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from ..config import ENV
from ..models import UserORM
from ..models.auth import TokenData, User
from ..utils import DBManager

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/secure/token")  # URL 주소 또는 로컬 Path 함수 경로

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = ENV.auth_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

logger = logging.getLogger(ENV.app_name)


def get_user(username: str):
    with DBManager() as engine:
        users = engine.session.query(UserORM).filter(UserORM.username == username).all()

    if not users:
        return None

    user_dict = users[0].as_dict()
    return User.model_validate(user_dict)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
