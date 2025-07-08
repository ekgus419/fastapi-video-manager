from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserDomain:
    email: str
    password: str
    role: str
    corporation_id: int
    point: int
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None