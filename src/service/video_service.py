from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user_domain import UserDomain
from src.domain.video_domain import VideoDomain
from src.dto.request.video_request_dto import VideoCreateRequestDto
from src.exception.user_exception import PermissionRestoreDeniedException
from src.mapper.video_mapper import entity_to_domain, domain_to_entity
from src.service.base_service import BaseService
from src.repository.video_repository import VideoRepository
from src.entity.video_entity import VideoEntity
from src.exception.video_exception import VideoNotFoundException
from src.service.corporation_service import CorporationService
from src.service.user_service import UserService


class VideoService(BaseService):
    def __init__(self, video_repository: VideoRepository):
        super().__init__(video_repository)
        self.video_repository = video_repository

    async def get_videos_by_corporation(self, db: AsyncSession, corporation_id: int) -> list[VideoDomain]:
        entities: list[VideoEntity] = await self.video_repository.find_by_corporation_id(db, corporation_id)
        return [entity_to_domain(e) for e in entities]

    async def get_video_by_id(self, db: AsyncSession, video_id: int) -> VideoDomain:
        entity: VideoEntity | None = await self.video_repository.find_by_id(db, video_id)
        if not entity:
            raise VideoNotFoundException()
        return entity_to_domain(entity)

    async def get_all_videos(self, db: AsyncSession) -> list[VideoDomain]:
        entities: list[VideoEntity] = list(await self.video_repository.find_all(db))
        return [entity_to_domain(e) for e in entities]

    async def get_by_corporation_id(self, db: AsyncSession, corporation_id: int) -> list[VideoDomain]:
        entities: list[VideoEntity] = await self.video_repository.find_by_corporation_id(db, corporation_id)
        return [entity_to_domain(e) for e in entities]

    async def create_video(self, db: AsyncSession, domain: VideoDomain) -> VideoDomain:
        entity: VideoEntity = domain_to_entity(domain)
        created: VideoEntity = await self.video_repository.save(db, entity)
        await db.commit()
        await db.refresh(created)
        return entity_to_domain(created)

    async def update_video(self, db: AsyncSession, video_id: int, values: dict) -> VideoDomain:
        existing = await self.video_repository.find_by_video_id(db, video_id)
        if not existing:
            raise VideoNotFoundException()

        entity: VideoEntity = await self.video_repository.update(db, video_id, **values)

        await db.commit()
        await db.refresh(entity)
        return entity_to_domain(entity)

    async def delete_video(self, db: AsyncSession, video_id: int) -> None:
        # 삭제 전 엔티티 먼저 조회
        existing = await self.video_repository.find_by_video_id(db, video_id)
        if not existing:
            raise VideoNotFoundException()

        # 삭제 수행
        await self.video_repository.update_delete_flags(
            db,
            video_id,
            is_deleted=True,
            deleted_at=func.now()
        )
        await db.commit()

    async def restore_video(
        self,
        db: AsyncSession,
        video_id: int,
        current_user: UserDomain,
        user_service: UserService,
        corporation_service: CorporationService
    ) -> VideoDomain:
        # 삭제된 영상 포함 조회
        video = await self.video_repository.find_by_video_id(db, video_id)
        if not video:
            raise VideoNotFoundException()

        # 유저의 소속 기업 → 유료 여부 확인
        user = await user_service.get_user_by_id(db, current_user.id)

        corp = await corporation_service.get_corporation_by_id(db, user.corporation_id)
        if corp.plan != "PAID":
            raise PermissionRestoreDeniedException()

        # 복구 처리
        video.is_deleted = False
        video.deleted_at = None
        await db.commit()
        await db.refresh(video)

        return entity_to_domain(video)
