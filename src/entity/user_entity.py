from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from src.entity.base_entity import BaseEntity


class UserEntity(BaseEntity):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(10), nullable=False)
    corporation_id: Mapped[int] = mapped_column(ForeignKey("corporation.id"), nullable=False)
    point: Mapped[int] = mapped_column(default=0)
    corporation: Mapped["CorporationEntity"] = relationship(back_populates="users")
    videos_viewed: Mapped[list["VideoViewLogEntity"]] = relationship(back_populates="user")
    tokens: Mapped[list["RefreshTokenEntity"]] = relationship(back_populates="user")
