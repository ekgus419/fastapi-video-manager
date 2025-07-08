from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.token_utils import get_current_user
from src.config.dependency_registry import get_video_view_log_service
from src.core.database import get_db_session
from src.dto.response.common_response_dto import CommonResponseDto
from src.service.video_view_log_service import VideoViewLogService
from src.domain.user_domain import UserDomain
from src.dto.request.video_view_log_request_dto import VideoViewLogCreateRequestDto, VideoViewLogUpdateRequestDto
from src.dto.response.video_view_log_response_dto import VideoViewLogResponseDto

router = APIRouter()

@router.get("/{user_id}/{video_id}", response_model=CommonResponseDto[bool])
async def has_user_viewed_video(
    user_id: int,
    video_id: int,
    db: AsyncSession = Depends(get_db_session),
    video_view_log_service: VideoViewLogService = Depends(get_video_view_log_service),
    current_user: UserDomain = Depends(get_current_user)
):
    """
    # 👁️ 회원의 영상 시청 여부 확인 API

    ## 📝 Args:
    - **`user_id`** (`int`): 회원 ID
    - **`video_id`** (`int`): 영상 ID

    ## 📤 Returns:
    - **`bool`**: 시청 여부 (`true` 또는 `false`)
    """
    viewed = await video_view_log_service.has_user_viewed_video(db, user_id, video_id)
    return CommonResponseDto(status="success", data=viewed)


@router.post("", response_model=CommonResponseDto[VideoViewLogResponseDto])
async def create_log(
    request: VideoViewLogCreateRequestDto,
    db: AsyncSession = Depends(get_db_session),
    video_view_log_service: VideoViewLogService = Depends(get_video_view_log_service),
    current_user: UserDomain = Depends(get_current_user)
):
    """
    # ➕ 시청 로그 생성 API

    ## 📝 Args:
    - **`VideoViewLogCreateRequestDto`**: 영상 ID

    ## ⚙️ 처리 내용:
    - 현재 로그인한 회원 ID + 전달된 영상 ID로 시청 로그 생성
    - `viewed_at`은 현재 시각으로 자동 기록

    ## 📤 Returns:
    - **`VideoViewLogResponseDto`**: 생성된 시청 로그 정보

    ## 🔐 권한:
    - 로그인된 회원만 생성 가능 (강제적으로 본인 user_id 사용)
    """
    created = await video_view_log_service.create_log(
        db,
        user_id=current_user.id,
        video_id=request.video_id
    )
    return CommonResponseDto(status="success", data=created)
