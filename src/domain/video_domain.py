from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class VideoDomain:
    name: str
    file_path: str
    corporation_id: int
    is_deleted: bool
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
