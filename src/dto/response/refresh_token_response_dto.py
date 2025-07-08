from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime


class RefreshTokenResponseDto(BaseModel):
    id: int = Field(..., description="리프레시 토큰 고유 ID")
    user_id: int = Field(..., description="해당 리프레시 토큰을 소유한 사용자 ID")
    token: str = Field(..., description="JWT 형식의 리프레시 토큰 문자열")
    expires_at: Optional[datetime] = Field(..., description="리프레시 토큰이 만료 시각")
    created_at: Optional[datetime] = Field(..., description="리프레시 토큰이 생성된 시각")