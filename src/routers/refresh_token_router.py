from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.dependency_registry import get_refresh_token_service
from src.core.database import get_db_session
from src.dto.response.common_response_dto import CommonResponseDto
from src.dto.response.refresh_token_response_dto import RefreshTokenResponseDto
from src.service.refresh_token_service import RefreshTokenService
from src.utils.token_utils import get_current_user
from src.domain.user_domain import UserDomain

router = APIRouter()

@router.get("/{user_id}", response_model=CommonResponseDto[RefreshTokenResponseDto])
async def get_token_by_user_id(
    user_id: int,
    db: AsyncSession = Depends(get_db_session),
    refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service),
    current_user: UserDomain = Depends(get_current_user)
):
    """
    # 🔐 사용자별 Refresh Token 조회 API

    ## 📝 Args:
    - **`user_id`** (`int`): 조회할 유저의 ID

    ## 📤 Returns:
    - **`RefreshTokenResponseDto`**: 해당 유저의 리프레시 토큰 정보

    ## ⚠️ Raises:
    - **`404 Not found`**: Refresh Token이 없는 경우
    - **`403 Forbidden`**: 관리자가 아닌 경우
    """
    token = await refresh_token_service.get_by_user_id(db, user_id)
    return CommonResponseDto(status="success", data=token)
