from datetime import datetime

from src.enums.corporation_enums import CorporationPlan
from src.repository.base_repository import BaseRepository
from src.entity.corporation_entity import CorporationEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete


class CorporationRepository(BaseRepository[CorporationEntity]):
    """
    CorporationEntity 전용 리포지토리.
    기본 CRUD는 BaseRepository에서 제공되며,
    도메인 특화 메서드를 여기에 정의합니다.
    """

    def __init__(self):
        super().__init__(CorporationEntity)

    async def find_by_name(self, db: AsyncSession, name: str) -> CorporationEntity | None:
        stmt = select(CorporationEntity).where(
            CorporationEntity.name == name,
            CorporationEntity.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def find_expired_paid_plans(self, db: AsyncSession, now: datetime) -> list[CorporationEntity]:
        result = await db.execute(
            select(CorporationEntity)
            .where(CorporationEntity.plan == CorporationPlan.PAID)
            .where(CorporationEntity.plan_expire_at < now)
            .where(CorporationEntity.deleted_at.is_(None))
        )
        return result.scalars().all()

