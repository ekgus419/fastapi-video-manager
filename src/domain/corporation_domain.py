from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CorporationDomain:
    name: str
    plan: str
    id: Optional[int] = None
    plan_expire_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
