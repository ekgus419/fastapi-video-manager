from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RefreshTokenDomain:
    user_id: int
    id: Optional[int] = None
    token: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


