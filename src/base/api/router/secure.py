import datetime
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from ...config import ENV
from ...constants import Color
from ...models import UserORM
from ...models.auth import CustomOAuth2PasswordRequestForm, Token, UserOutput
from ...utils import DBManager
from ...utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, get_current_active_user, get_user
from ...utils.common import get_password_hash, verify_password

# to get a string like this run:
# openssl rand -hex 32

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/secure/token")  # URL 주소 또는 로컬 Path 함수 경로

router = APIRouter(
    prefix="/secure",
    tags=["Secure APIs"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)
logger = logging.getLogger(ENV.app_name)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: CustomOAuth2PasswordRequestForm = Depends()):
    def authenticate_user(username: str, password: str):
        auth_user = get_user(username=username)
        if not auth_user:
            return False
        if not verify_password(plain_password=password, hashed_password=auth_user.password):
            return False
        return auth_user

    def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    """
    User 인증 및 토큰 생성 코드
    """
    try:
        username = form_data.username
        password = form_data.password.get_secret_value()
        user = authenticate_user(username=username, password=password)
    except Exception as e:
        logger.error(f"{Color.RED}{e}{Color.DEFAULT}")
    else:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        pass


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    current_user: UserOutput = Depends(get_current_active_user), form_data: CustomOAuth2PasswordRequestForm = Depends()
):
    try:
        username = form_data.username
        password = form_data.password.get_secret_value()
        user_item = UserORM(username=username, password=get_password_hash(password))

        with DBManager() as engine:
            _ = engine.insert(items=user_item)

        return None

    except Exception as e:
        logger.error(f"{Color.RED}{e}{Color.DEFAULT}")
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create user")


@router.get("/users/me/", response_model=UserOutput)
async def read_users_me(current_user: UserOutput = Depends(get_current_active_user)):
    return current_user
