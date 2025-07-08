from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import DateTime, func


class BaseEntity(DeclarativeBase):
    """
    모든 ORM 모델이 상속받는 공통 베이스 클래스.
    """
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
