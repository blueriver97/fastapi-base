from typing import Optional
from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from base.config import settings

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Mock 데이터베이스 ---
# 실제 인증 시스템이 구현되기 전까지 사용할 임시 클라이언트 정보입니다.
# '비밀번호'는 실제 값 대신 해시된 값을 저장합니다.
MOCK_CLIENTS_DB = {settings.app.auth.root_user: {"hashed_secret": pwd_context.hash(settings.app.auth.root_password)}}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """일반 비밀번호와 해시된 비밀번호를 비교합니다."""
    return pwd_context.verify(plain_password, hashed_password)


def validate_client_credentials(client_id: str, client_secret: str) -> Optional[str]:
    """
    클라이언트 자격증명을 확인합니다. (Mock 버전)
    성공 시 client_id를, 실패 시 None을 반환합니다.
    """
    client_data = MOCK_CLIENTS_DB.get(client_id)
    if not client_data:
        return None

    if not verify_password(client_secret, client_data["hashed_secret"]):
        return None

    # 인증 성공 시, 객체 대신 클라이언트 ID 문자열만 반환
    return client_id


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """액세스 토큰을 생성합니다."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(seconds=settings.app.auth.token_expire_seconds)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.app.auth.secret_key, algorithm=settings.app.auth.algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> str:
    """
    Validates and decodes the JWT token to extract the subject (client_id).
    JWT 토큰을 검증하고 디코딩하여 subject (client_id)를 추출합니다.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.app.auth.secret_key, algorithms=[settings.app.auth.algorithm])
        client_id: Optional[str] = payload.get("sub")
        if client_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return client_id
