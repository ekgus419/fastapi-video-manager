from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text
from src.entity.base_entity import BaseEntity


class VideoEntity(BaseEntity):
    __tablename__ = "video"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    corporation_id: Mapped[int] = mapped_column(ForeignKey("corporation.id"), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    corporation: Mapped["CorporationEntity"] = relationship(back_populates="videos")
    view_logs: Mapped[list["VideoViewLogEntity"]] = relationship(back_populates="video")
