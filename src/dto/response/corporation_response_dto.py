from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CorporationResponseDto(BaseModel):
    id: int = Field(..., description="기업 ID")
    name: str = Field(..., description="기업명")
    plan: str = Field(..., description="플랜 상태")
    plan_expire_at: Optional[datetime] = Field(None, description="플랜 만료일")
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
