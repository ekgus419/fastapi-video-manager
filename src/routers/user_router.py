from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.dto.request.user_request_dto import UserCreateRequestDto, UserUpdateRequestDto
from src.utils.token_utils import get_current_user

from src.config.dependency_registry import get_user_service
from src.core.database import get_db_session
from src.dto.response.common_response_dto import CommonResponseDto
from src.dto.response.user_response_dto import UserResponseDto
from src.service.user_service import UserService
from src.domain.user_domain import UserDomain

router = APIRouter()

@router.get("/{email}", response_model=CommonResponseDto[UserResponseDto])
async def get_user_by_email(
    email: EmailStr,
    db: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service),
    current_user: UserDomain = Depends(get_current_user)
):
    """
    # 👤 회원 이메일로 조회 API

    ## 📝 Args:
    - **`email`** (`EmailStr`): 조회할 회원 이메일

    ## 📤 Returns:
    - **`UserResponseDto`**: 해당 이메일을 가진 회원 정보

    ## ⚠️ Raises:
    - **`404 Not Found`**: 회원이 존재하지 않는 경우
    """
    user = await user_service.get_user_by_email(db, email)
    return CommonResponseDto(status="success", data=user)

@router.post("", response_model=CommonResponseDto[UserResponseDto])
async def create_user(
    request: UserCreateRequestDto,
    db: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service)
):
    """
    # ➕ 회원 생성 API

    ## 📝 Args:
    - **`request`**: 이메일, 비밀번호, 권한, 기업 ID 등

    ## 📤 Returns:
    - **`UserResponseDto`**: 생성된 회원 정보

    ## ⚠️ Raises:
    - **`409 Conflict`**: 같은 기업 내에 이미 존재하는 이메일인 경우
    """
    created = await user_service.create_user(db, request)
    return CommonResponseDto(status="success", data=created)

@router.get("/id/{user_id}", response_model=CommonResponseDto[UserResponseDto])
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service),
    current_user: UserDomain = Depends(get_current_user)
):
    """
    # 🔍 회원 단건 조회 API

    ## 📝 Args:
    - **`user_id`** (`int`): 회원 ID

    ## 📤 Returns:
    - **`UserResponseDto`**: 해당 ID의 회원 정보

    ## ⚠️ Raises:
    - **`404 Not Found`**: 회원이 존재하지 않는 경우
    """
    user = await user_service.get_user_by_id(db, user_id)
    return CommonResponseDto(status="success", data=user)

@router.get("", response_model=CommonResponseDto[list[UserResponseDto]])
async def get_all_users(
    db: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service),
    current_user: UserDomain = Depends(get_current_user)
):
    """
    # 📋 전체 회원 목록 조회 API

    ## 📤 Returns:
    - **`List[UserResponseDto]`**: 전체 회원 목록
    """
    users = await user_service.get_all_users(db)
    return CommonResponseDto(status="success", data=users)

@router.put("/{user_id}", response_model=CommonResponseDto[UserResponseDto])
async def update_user(
    user_id: int,
    request: UserUpdateRequestDto,
    db: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service),
    current_user: UserDomain = Depends(get_current_user),
):
    """
    # ✏️ 회원 정보 수정 API

    ## 📝 Args:
    - **`user_id`** (`int`): 수정 대상 회원 ID
    - **`request`** (`dict`): 변경할 값들 (비밀번호, 권한 등)

    ## 📤 Returns:
    - **`UserResponseDto`**: 수정된 회원 정보

    ## 🔐 Permission:
    - 본인 또는 같은 기업의 관리자만 수정 가능

    ## ⚠️ Raises:
    - **`404 Not Found`**: 회원이 존재하지 않는 경우
    - **`403 Forbidden`**: 같은 기업이고 admin 권한이 아닌 경우
    """
    updated = await user_service.update_user(db, user_id, request, current_user)
    return CommonResponseDto(status="success", data=updated)

@router.delete("/{user_id}", response_model=CommonResponseDto[bool])
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service),
    current_user: UserDomain = Depends(get_current_user),
):
    """
    # ❌ 회원 삭제 API

    ## 📝 Args:
    - **`user_id`** (`int`): 삭제할 회원 ID

    ## 📤 Returns:
    - **`UserResponseDto`**: 삭제된 회원 정보 (soft delete)

    ## 🔐 Permission:
    - 본인 또는 같은 기업의 관리자만 삭제 가능

    ## ⚠️ Raises:
    - **`404 Not Found`**: 회원이 존재하지 않는 경우
    - **`403 Forbidden`**: 삭제 권한이 없는 경우
    """
    await user_service.delete_user(db, user_id, current_user)
    return CommonResponseDto(status="success", data=True)
