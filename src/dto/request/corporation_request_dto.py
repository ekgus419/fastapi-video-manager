from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

from src.enums.corporation_enums import CorporationPlan


class CorporationCreateRequestDto(BaseModel):
    name: str = Field(..., description="기업명")
    plan: CorporationPlan = Field(..., description="플랜 (FREE or PAID)")
    plan_expire_at: Optional[datetime] = Field(None, description="유료 플랜 만료일")

    admin_email: str = Field(..., description="최초 관리자 이메일")
    admin_password: str = Field(..., description="최초 관리자 비밀번호")


class CorporationUpdateRequestDto(BaseModel):
    name: Optional[str] = Field(None, description="기업명")
    plan: Optional[CorporationPlan] = Field(None, description="플랜 변경")
    plan_expire_at: Optional[datetime] = Field(None, description="플랜 만료일 변경")
