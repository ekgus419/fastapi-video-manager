from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey
from datetime import datetime

from src.entity.base_entity import BaseEntity


class RefreshTokenEntity(BaseEntity):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    token: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[datetime]
    user: Mapped["UserEntity"] = relationship(back_populates="tokens")
