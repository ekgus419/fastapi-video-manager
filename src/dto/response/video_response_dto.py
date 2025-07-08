from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class VideoResponseDto(BaseModel):
    id: int = Field(..., description="영상 ID")
    name: str = Field(..., description="영상 이름")
    file_path: str = Field(..., description="파일 경로")
    corporation_id: int = Field(..., description="소속 기업 ID")
    is_deleted: bool = Field(..., description="삭제 여부")
    created_at: Optional[datetime] = Field(..., description="생성일시")
    updated_at: Optional[datetime] = Field(..., description="수정일시")
    deleted_at: Optional[datetime] = Field(None, description="삭제일시 (nullable)")
