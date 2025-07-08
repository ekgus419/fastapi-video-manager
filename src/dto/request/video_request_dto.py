from pydantic import BaseModel, Field
from typing import Optional


class VideoCreateRequestDto(BaseModel):
    name: str = Field(..., description="영상 이름")
    file_path: str = Field(..., description="파일 경로")
    corporation_id: int = Field(..., description="소속 기업 ID")


class VideoUpdateRequestDto(BaseModel):
    name: Optional[str] = Field(None, description="영상 이름")
    file_path: Optional[str] = Field(None, description="파일 경로")
