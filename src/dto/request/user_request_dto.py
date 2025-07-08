from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

from src.enums.user_enums import UserRole

class UserCreateRequestDto(BaseModel):
    email: EmailStr = Field(..., description="사용자 이메일")
    password: str = Field(..., min_length=6, description="비밀번호")
    role: UserRole = Field(..., description="사용자 권한 (admin 또는 guest)")
    point: int = Field(0, description="포인트")
    corporation_id: int = Field(..., description="소속 기업 ID")

class UserUpdateRequestDto(BaseModel):
    password: Optional[str] = Field(None, min_length=6, description="비밀번호 변경 (선택)")
    role: Optional[UserRole] = Field(None, description="권한 변경 (admin 또는 guest)")
