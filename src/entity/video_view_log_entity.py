from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func, UniqueConstraint
from datetime import datetime
from src.entity.base_entity import BaseEntity


class VideoViewLogEntity(BaseEntity):
    __tablename__ = "video_view_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    video_id: Mapped[int] = mapped_column(ForeignKey("video.id"), nullable=False)
    user: Mapped["UserEntity"] = relationship(back_populates="videos_viewed")
    video: Mapped["VideoEntity"] = relationship(back_populates="view_logs")
    viewed_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "video_id", name="uq_user_video_once"),
    )