from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

class VideoViewLogResponseDto(BaseModel):
    id: int = Field(..., description="조회 로그 ID")
    user_id: int = Field(..., description="조회한 사용자 ID")
    video_id: int = Field(..., description="조회된 영상 ID")
    viewed_at: Optional[datetime] = Field(..., description="조회 시각")
