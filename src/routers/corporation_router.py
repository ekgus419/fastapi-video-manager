from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.dependency_registry import get_corporation_service, get_user_service
from src.core.database import get_db_session
from src.dto.request.corporation_request_dto import CorporationCreateRequestDto, CorporationUpdateRequestDto
from src.dto.response.common_response_dto import CommonResponseDto
from src.dto.response.corporation_response_dto import CorporationResponseDto
from src.service.user_service import UserService
from src.utils.token_utils import get_current_active_admin
from src.domain.user_domain import UserDomain
from src.service.corporation_service import CorporationService

router = APIRouter()

@router.get("/{name}", response_model=CommonResponseDto[CorporationResponseDto])
async def get_corporation_by_name(
    name: str,
    db: AsyncSession = Depends(get_db_session),
    corporation_service: CorporationService = Depends(get_corporation_service)
):
    """
    # 🏢 기업 이름으로 단건 조회 API

    ## 📝 Args:
    - **`name`** (`str`): 조회할 기업 이름

    ## 📤 Returns:
    - **`CorporationResponseDto`**: 해당 이름을 가진 기업 정보

    ## ⚠️ Raises:
    - **`404 Not Found`**: 기업명이 존재하지 않는 기업인 경우
    """
    domain = await corporation_service.get_corporation_by_name(db, name)
    return CommonResponseDto(status="success", data=domain)

@router.post("", response_model=CommonResponseDto[CorporationResponseDto])
async def create_corporation(
    request: CorporationCreateRequestDto,
    db: AsyncSession = Depends(get_db_session),
    corporation_service: CorporationService = Depends(get_corporation_service),
    user_service: UserService = Depends(get_user_service)
):
    """
    # 🏢 기업 생성 + 관리자 계정 등록 API

    ## 📝 Args:
    - **`request`**: 기업명, 플랜, 만료일, 관리자 이메일/비밀번호 포함

    ## 📤 Returns:
    - **`CorporationResponseDto`**: 생성된 기업 정보

    ## ⚠️ Raises:
    - **`400 Conflict`**: 중복된 기업명이 존재할 경우
    """
    created = await corporation_service.create_corporation(
        db,
        request,
        admin_email=request.admin_email,
        admin_password=request.admin_password,
        user_service=user_service
    )
    return CommonResponseDto(status="success", data=created)

@router.get("/id/{corporation_id}", response_model=CommonResponseDto[CorporationResponseDto])
async def get_corporation_by_id(
    corporation_id: int,
    db: AsyncSession = Depends(get_db_session),
    corporation_service: CorporationService = Depends(get_corporation_service)
):
    """
    # 🔍 기업 ID로 단건 조회 API

    ## 📝 Args:
    - **`corporation_id`** (`int`): 조회할 기업 ID

    ## 📤 Returns:
    - **`CorporationResponseDto`**: 해당 ID의 기업 정보

    ## ⚠️ Raises:
    - **`404 Not Found`**: 존재하지 않는 기업인 경우
    """
    corporation = await corporation_service.get_corporation_by_id(db, corporation_id)
    return CommonResponseDto(status="success", data=corporation)

@router.get("", response_model=CommonResponseDto[list[CorporationResponseDto]])
async def get_all_corporations(
    db: AsyncSession = Depends(get_db_session),
    corporation_service: CorporationService = Depends(get_corporation_service)
):
    """
    # 📋 전체 기업 목록 조회 API

    ## 📤 Returns:
    - **`List[CorporationResponseDto]`**: 전체 기업 정보 목록
    """
    corporations = await corporation_service.get_all_corporations(db)
    return CommonResponseDto(status="success", data=corporations)

@router.put("/{corporation_id}", response_model=CommonResponseDto[CorporationResponseDto])
async def update_corporation(
    corporation_id: int,
    request: CorporationUpdateRequestDto,
    db: AsyncSession = Depends(get_db_session),
    corporation_service: CorporationService = Depends(get_corporation_service),
    current_user: UserDomain = Depends(get_current_active_admin)
):
    """
    # ✏️ 기업 정보 수정 API

    ## 📝 Args:
    - **`corporation_id`** (`int`): 수정할 기업 ID
    - **`request`**: 기업명, 플랜, 만료일

    ## 📤 Returns:
    - **`CorporationResponseDto`**: 수정된 기업 정보

    ## ⚠️ Raises:
    - **`400 Conflict`**: 중복된 기업명이 존재할 경우
    - **`403 Forbidden`**: 관리자가 아닌 경우
    """
    updated = await corporation_service.update_corporation(db, corporation_id, request)
    return CommonResponseDto(status="success", data=updated)

@router.delete("/{corporation_id}", response_model=CommonResponseDto[bool])
async def delete_corporation(
    corporation_id: int,
    db: AsyncSession = Depends(get_db_session),
    corporation_service: CorporationService = Depends(get_corporation_service),
    current_user: UserDomain = Depends(get_current_active_admin)
):
    """
    # ❌ 기업 삭제 API

    ## 📝 Args:
    - **`corporation_id`** (`int`): 삭제할 기업 ID

    ## 📤 Returns:
    - **`CorporationResponseDto`**: 삭제된 기업 정보

    ## ⚠️ Raises:
    - **`403 Forbidden`**: 관리자가 아닌 경우
    - **`404 Not Found`**: 기업이 존재하지 않을 경우
    """
    await corporation_service.delete_corporation(db, corporation_id)
    return CommonResponseDto(status="success", data=True)
