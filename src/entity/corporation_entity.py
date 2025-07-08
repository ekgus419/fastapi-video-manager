from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from datetime import datetime

from src.entity.base_entity import BaseEntity


class CorporationEntity(BaseEntity):
    __tablename__ = "corporation"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    plan: Mapped[str] = mapped_column(String(10), nullable=False)
    plan_expire_at: Mapped[datetime | None]
    users: Mapped[list["UserEntity"]] = relationship(back_populates="corporation")
    videos: Mapped[list["VideoEntity"]] = relationship(back_populates="corporation")
