from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class VideoViewLogDomain:
    user_id: int
    video_id: int
    id: Optional[int] = None
    viewed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
