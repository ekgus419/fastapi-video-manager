from datetime import datetime

from sqlalchemy.exc import IntegrityError

from src.domain.video_view_log_domain import VideoViewLogDomain
from src.mapper.video_view_log_mapper import entity_to_domain, domain_to_entity
from sqlalchemy.ext.asyncio import AsyncSession
from src.service.base_service import BaseService
from src.repository.video_view_log_repository import VideoViewLogRepository
from src.entity.video_view_log_entity import VideoViewLogEntity


class VideoViewLogService(BaseService):
    def __init__(self, video_view_log_repository: VideoViewLogRepository):
        super().__init__(video_view_log_repository)
        self.video_view_log_repository = video_view_log_repository

    async def has_user_viewed_video(self, db: AsyncSession, user_id: int, video_id: int) -> bool:
        return await self.video_view_log_repository.has_user_viewed_video(db, user_id, video_id)

    async def create_log(self, db: AsyncSession, user_id: int, video_id: int) -> VideoViewLogDomain:
        domain = VideoViewLogDomain(
            user_id=user_id,
            video_id=video_id,
            viewed_at=datetime.utcnow()
        )
        entity: VideoViewLogEntity = domain_to_entity(domain)
        try:
            created = await self.video_view_log_repository.save(db, entity)
            await db.commit()
            await db.refresh(created)
            return entity_to_domain(created)
        except IntegrityError:
            await db.rollback()
            raise  # Router에서 처리할 수 있도록 그대로 전파