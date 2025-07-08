from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class VideoViewLogCreateRequestDto(BaseModel):
    video_id: int = Field(..., description="비디오 ID")

class VideoViewLogUpdateRequestDto(BaseModel):
    viewed_at: Optional[datetime] = Field(None, description="시청 시각")
