
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.dependency_registry import get_user_service, get_refresh_token_service
from src.core.database import get_db_session
from src.domain.refreshtoken_domain import RefreshTokenDomain
from src.dto.request.token_refresh_request_dto import RefreshRequestDto
from src.dto.request.token_request_dto import LoginRequestDto
from src.dto.response.common_response_dto import CommonResponseDto
from src.dto.response.token_response_dto import TokenPairResponseDto
from src.exception.refresh_token_exception import InvalidRefreshTokenException, RefreshTokenDecodeException
from src.exception.user_exception import InvalidCredentialsException
from src.service.user_service import UserService
from src.service.refresh_token_service import RefreshTokenService
from src.utils import jwt_utils

router = APIRouter()

@router.post("/login", response_model=CommonResponseDto[TokenPairResponseDto])
async def login(
    request: LoginRequestDto,
    db: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service),
    refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service)
):
    """
    # 🔐 로그인 API

    ## 📝 Args:
    - **`request`** (`LoginRequestDto`): 이메일과 비밀번호

    ## 📤 Returns:
    - **`CommonResponseDto[TokenPairResponseDto]`**:
      - Access Token과 Refresh Token 페어 반환

    ## ⚠️ Raises:
    - **`401 Unauthorized`**: 이메일 또는 비밀번호가 잘못된 경우
    """
    user = await user_service.verify_credentials(db, request.email, request.password)
    if not user:
        raise InvalidCredentialsException()

    access_token = jwt_utils.create_access_token(data={"sub": str(user.id)})
    refresh_token = jwt_utils.create_refresh_token(data={"sub": str(user.id)})

    await refresh_token_service.create_token(db, RefreshTokenDomain(
        user_id=user.id,
        token=refresh_token
    ))

    return CommonResponseDto(
        status="success",
        data=TokenPairResponseDto(
            access_token=access_token,
            refresh_token=refresh_token
        )
    )
@router.post("/refresh", response_model=CommonResponseDto[TokenPairResponseDto])
async def refresh_token(
    request: RefreshRequestDto,
    db: AsyncSession = Depends(get_db_session),
    refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service)
):
    """
    # 🔁 Refresh Token 갱신 API

    ## 📝 Args:
    - **`request`** (`RefreshRequestDto`): 기존 리프레시 토큰

    ## 📤 Returns:
    - **`CommonResponseDto[TokenPairResponseDto]`**:
      - 새로운 Access Token + 기존 Refresh Token 반환

    ## ⚠️ Raises:
    - **`401 Unauthorized`**:
      - Refresh Token 디코딩 실패
      - 저장된 토큰과 불일치
    """
    try:
        payload = jwt_utils.decode_token(request.refresh_token)
        user_id = int(payload.get("sub"))
    except Exception as e:
        raise RefreshTokenDecodeException()

    stored = await refresh_token_service.get_token_by_user_id(db, user_id)
    if not stored or stored.token != request.refresh_token:
        raise InvalidRefreshTokenException()
    new_access_token = jwt_utils.create_access_token(data={"sub": str(user_id)})
    return CommonResponseDto(
        status="success",
        data=TokenPairResponseDto(
            access_token=new_access_token,
            refresh_token=request.refresh_token
        )
    )
