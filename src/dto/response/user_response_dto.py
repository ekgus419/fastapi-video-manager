from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserResponseDto(BaseModel):
    id: int = Field(..., description="유저 고유 ID")
    email: EmailStr = Field(..., description="이메일")
    role: str = Field(..., description="사용자 권한")
    corporation_id: int = Field(..., description="소속 기업 ID")
    point: int = Field(..., description="포인트")
    created_at: Optional[datetime] = Field(..., description="생성일")
    updated_at: Optional[datetime] = Field(..., description="수정일")
    deleted_at: Optional[datetime] = Field(None, description="삭제일 (논리삭제)")
