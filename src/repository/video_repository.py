from datetime import datetime

from src.repository.base_repository import BaseRepository
from src.entity.video_entity import VideoEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete


class VideoRepository(BaseRepository[VideoEntity]):
    """
    VideoEntity 전용 리포지토리.
    기본 CRUD는 BaseRepository에서 제공되며,
    도메인 특화 메서드를 여기에 정의합니다.
    """

    def __init__(self):
        super().__init__(VideoEntity)

    async def find_by_corporation_id(self, db: AsyncSession, corporation_id: int) -> list[VideoEntity]:
        stmt = select(VideoEntity).where(
            VideoEntity.corporation_id == corporation_id,
            VideoEntity.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def find_by_video_id(self, db: AsyncSession, video_id: int) -> VideoEntity | None:
        stmt = select(VideoEntity).where(VideoEntity.id == video_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def update_delete_flags(
        self,
        db: AsyncSession,
        video_id: int,
        is_deleted: bool,
        deleted_at: datetime | None
    ) -> VideoEntity | None:
        video = await self.find_by_video_id(db, video_id)
        if not video:
            return None
        video.is_deleted = is_deleted
        video.deleted_at = deleted_at
        return video
