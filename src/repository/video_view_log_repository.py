from src.repository.base_repository import BaseRepository
from src.entity.video_view_log_entity import VideoViewLogEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete


class VideoViewLogRepository(BaseRepository[VideoViewLogEntity]):
    """
    VideoViewLogEntity 전용 리포지토리.
    기본 CRUD는 BaseRepository에서 제공되며,
    도메인 특화 메서드를 여기에 정의합니다.
    """

    def __init__(self):
        super().__init__(VideoViewLogEntity)

    async def has_user_viewed_video(self, db: AsyncSession, user_id: int, video_id: int) -> bool:
        stmt = select(VideoViewLogEntity).where(
            VideoViewLogEntity.user_id == user_id,
            VideoViewLogEntity.video_id == video_id
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def find_by_log_id(self, db: AsyncSession, log_id: int) -> VideoViewLogEntity | None:
        stmt = select(VideoViewLogEntity).where(VideoViewLogEntity.id == log_id)
        result = await db.execute(stmt)
        return result.scalars().first()