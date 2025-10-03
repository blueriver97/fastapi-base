import datetime
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from base.utils.auth import validate_client_credentials, create_access_token, decode_access_token
from base.config import settings

logger = logging.getLogger(__name__)

# tokenUrl은 이 엔드포인트의 경로와 일치해야 합니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)


class Token(BaseModel):
    access_token: str
    token_type: str


async def get_current_client_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependency to decode and validate the access token.
    액세스 토큰을 디코딩하고 검증하는 의존성 함수.

    This function is injected into protected endpoints. FastAPI handles
    extracting the Bearer token from the Authorization header and passing
    it to this function.
    이 함수는 보호된 엔드포인트에 주입됩니다. FastAPI는 Authorization 헤더에서
    Bearer 토큰을 추출하여 이 함수에 전달하는 과정을 처리합니다.
    """
    return decode_access_token(token=token)


@router.post("/token", response_model=Token)
async def issue_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    클라이언트 자격증명(Client Credentials)을 확인하고 액세스 토큰을 발급합니다.
    - username 필드에 'Client ID'를,
    - password 필드에 'Client Secret'을 담아 요청합니다.
    """

    # 1. 클라이언트 인증 (범용 인증 유틸리티 함수 사용)
    # FastAPI의 OAuth2PasswordRequestForm은 'username', 'password' 필드를 사용하므로
    # 이를 각각 client_id와 client_secret으로 간주하고 사용합니다.
    client_id = validate_client_credentials(client_id=form_data.username, client_secret=form_data.password)

    # 2. 인증 실패 시 예외 처리
    if not client_id:
        logger.warning(f"Authentication failed for client: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. 액세스 토큰 생성 (JWT의 sub 클레임에 client_id 사용)
    access_token_expires = datetime.timedelta(seconds=settings.app.auth.token_expire_seconds)
    access_token = create_access_token(data={"sub": client_id}, expires_delta=access_token_expires)

    logger.info(f"Token issued for client: {client_id}")

    # 4. 토큰 반환
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=dict)
async def read_current_client_info(
    current_client_id: str = Depends(get_current_client_id),
):
    """
    Retrieves information for the currently authenticated client.
    This endpoint is protected and requires a valid Bearer token.

    현재 인증된 클라이언트의 정보를 가져옵니다.
    이 엔드포인트는 보호되어 있으며, 유효한 Bearer 토큰이 필요합니다.
    """
    # In a real application, you might use this ID to look up more client details.
    # 실제 애플리케이션에서는 이 ID를 사용하여 더 많은 클라이언트 정보를 조회할 수 있습니다.
    return {"client_id": current_client_id, "status": "active"}
