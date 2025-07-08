import httpx

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exception.video_exception import VideoStreamingFailedException
from src.service.corporation_service import CorporationService
from src.service.user_service import UserService
from src.service.video_view_log_service import VideoViewLogService
from src.utils.token_utils import get_current_user, get_current_active_admin

from src.config.dependency_registry import get_video_service, get_video_view_log_service, get_user_service, \
    get_corporation_service
from src.core.database import get_db_session
from src.dto.response.common_response_dto import CommonResponseDto
from src.dto.response.video_response_dto import VideoResponseDto
from src.service.video_service import VideoService
from src.dto.request.video_request_dto import VideoCreateRequestDto, VideoUpdateRequestDto
from src.domain.user_domain import UserDomain

router = APIRouter()

@router.get("/stream/{video_id}", response_class=StreamingResponse)
async def stream_video(
    video_id: int,
    db: AsyncSession = Depends(get_db_session),
    video_service: VideoService = Depends(get_video_service),
    video_view_log_service: VideoViewLogService = Depends(get_video_view_log_service),
    user_service: UserService = Depends(get_user_service),
    current_user: UserDomain = Depends(get_current_user)
):
    """
    # 🎥 영상 스트리밍 API

    ## 📝 Args:
    - **`video_id`** (`int`): 스트리밍할 영상 ID

    ## ⚙️ 기능:
    - 시청 기록 생성 (`VideoViewLog`)
    - 유저에게 10포인트 지급
    - 외부 URL에서 영상 받아 프록시 스트리밍

    ## 📤 Returns:
    - **`StreamingResponse`**: mp4 형식의 영상 스트림

    ## ⚠️ Raises:
    - **`404 Not Found`**: 영상이 존재하지 않을 경우
    - **`404 Not Found`**: 회원이 존재하지 않을 경우
    - **`502 Bad Gateway`**: 영상 스트리밍 요청 실패 시
    """
    # 1. 영상 정보 조회
    video = await video_service.get_video_by_id(db, video_id)

    # 2. 시청 로그 및 포인트 지급
    try:
        await video_view_log_service.create_log(db, current_user.id, video_id)
    except IntegrityError:
        await db.rollback()  # 이미 본 영상 → 무시
    else:
        await user_service.add_point(db, current_user.id, 10)

    # 3. 외부 URL → StreamingResponse 으로 중계
    try:
        client = httpx.AsyncClient()
        response = await client.get(video.file_path, timeout=10.0)
        return StreamingResponse(
            content=response.aiter_bytes(),
            media_type="video/mp4"
        )
    except httpx.HTTPError as e:
        raise VideoStreamingFailedException()

@router.get("/{corporation_id}", response_model=CommonResponseDto[list[VideoResponseDto]])
async def get_videos_by_corporation(
    corporation_id: int,
    db: AsyncSession = Depends(get_db_session),
    video_service: VideoService = Depends(get_video_service),
    current_user: UserDomain = Depends(get_current_user)
):
    """
    # 🏢 기업별 영상 목록 조회 API

    ## 📝 Args:
    - **`corporation_id`** (`int`): 기업 ID

    ## 📤 Returns:
    - **`List[VideoResponseDto]`**: 해당 기업이 등록한 모든 영상 목록
    """
    videos = await video_service.get_videos_by_corporation(db, corporation_id)
    return CommonResponseDto(status="success", data=videos)

@router.post("", response_model=CommonResponseDto[VideoResponseDto])
async def create_video(
    request: VideoCreateRequestDto,
    db: AsyncSession = Depends(get_db_session),
    video_service: VideoService = Depends(get_video_service),
    current_user: UserDomain = Depends(get_current_active_admin)
):
    """
    # ➕ 관리자 전용 영상 등록 API

    ## 📝 Args:
    - **`request`**: 영상명, 파일 경로, 소속 기업 ID

    ## 📤 Returns:
    - **`VideoResponseDto`**: 등록된 영상 정보
    """
    created = await video_service.create_video(db, request)
    return CommonResponseDto(status="success", data=created)

@router.get("/id/{video_id}", response_model=CommonResponseDto[VideoResponseDto])
async def get_video_by_id(
    video_id: int,
    db: AsyncSession = Depends(get_db_session),
    video_service: VideoService = Depends(get_video_service)
):
    """
    # 🔍 영상 단건 조회 API

    ## 📝 Args:
    - **`video_id`** (`int`): 조회할 영상 ID

    ## 📤 Returns:
    - **`VideoResponseDto`**: 영상 정보

    ## ⚠️ Raises:
    - **`404 Not Found`**: 영상이 존재하지 않을 경우
    """
    video = await video_service.get_video_by_id(db, video_id)
    return CommonResponseDto(status="success", data=video)

@router.get("", response_model=CommonResponseDto[list[VideoResponseDto]])
async def get_all_videos(
    db: AsyncSession = Depends(get_db_session),
    video_service: VideoService = Depends(get_video_service)
):
    """
    # 📋 전체 영상 목록 조회 API

    ## 📤 Returns:
    - **`List[VideoResponseDto]`**: 전체 영상 목록
    """
    videos = await video_service.get_all_videos(db)
    return CommonResponseDto(status="success", data=videos)

@router.put("/{video_id}", response_model=CommonResponseDto[VideoResponseDto])
async def update_video(
    video_id: int,
    request: VideoUpdateRequestDto,
    db: AsyncSession = Depends(get_db_session),
    video_service: VideoService = Depends(get_video_service),
    current_user: UserDomain = Depends(get_current_active_admin)
):
    """
    # ✏️ 관리자 영상 정보 수정 API

    ## 📝 Args:
    - **`video_id`** (`int`): 수정 대상 영상 ID
    - **`request`**: 변경할 영상명 or 파일경로

    ## 📤 Returns:
    - **`VideoResponseDto`**: 수정된 영상 정보

    ## ⚠️ Raises:
    - **`404 Not Found`**: 영상이 존재하지 않을 경우
    """
    updated = await video_service.update_video(db, video_id, request.model_dump(exclude_unset=True))
    return CommonResponseDto(status="success", data=updated)

@router.delete("/{video_id}", response_model=CommonResponseDto[bool])
async def delete_video(
    video_id: int,
    db: AsyncSession = Depends(get_db_session),
    video_service: VideoService = Depends(get_video_service),
    current_user: UserDomain = Depends(get_current_active_admin)
):
    """
    # ❌ 관리자 영상 삭제 API

    ## 📝 Args:
    - **`video_id`** (`int`): 삭제할 영상 ID

    ## 📤 Returns:
    - **`bool`**: 성공 여부 (always true)

    ## ⚠️ Raises:
    - **`404 Not Found`**: 영상이 존재하지 않을 경우
    """
    await video_service.delete_video(db, video_id)
    return CommonResponseDto(status="success", data=True)

@router.put("/{video_id}/restore", response_model=CommonResponseDto[VideoResponseDto])
async def restore_video(
    video_id: int,
    db: AsyncSession = Depends(get_db_session),
    video_service: VideoService = Depends(get_video_service),
    user_service: UserService = Depends(get_user_service),
    corporation_service: CorporationService = Depends(get_corporation_service),
    current_user: UserDomain = Depends(get_current_active_admin)
):
    """
    # ♻️ 관리자 삭제된 영상 복구 API

    ## 📝 Args:
    - **`video_id`** (`int`): 복구할 영상 ID

    ## ⚙️ 조건:
    - 영상은 삭제 상태여야 함
    - 해당 유저의 소속 기업이 **유료(PAID)** 플랜이어야 복구 가능

    ## 📤 Returns:
    - **`VideoResponseDto`**: 복구된 영상 정보

    ## ⚠️ Raises:
    - **`404 Not Found`**: 영상이 존재하지 않을 경우
    - **`403 Forbidden`**: 복구 권한이 없는경우 (PAID)
    """
    restored = await video_service.restore_video(
        db=db,
        video_id=video_id,
        current_user=current_user,
        user_service=user_service,
        corporation_service=corporation_service
    )
    return CommonResponseDto(status="success", data=restored)

