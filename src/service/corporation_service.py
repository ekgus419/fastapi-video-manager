from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.corporation_domain import CorporationDomain
from src.domain.user_domain import UserDomain
from src.dto.request.corporation_request_dto import CorporationCreateRequestDto, CorporationUpdateRequestDto
from src.enums.corporation_enums import CorporationPlan
from src.enums.user_enums import UserRole
from src.exception.corporation_exception import CorporationNotFoundException, CorporationNameDuplicateException
from src.mapper.corporation_mapper import entity_to_domain, domain_to_entity
from src.service.base_service import BaseService
from src.repository.corporation_repository import CorporationRepository
from src.entity.corporation_entity import CorporationEntity
from src.service.user_service import UserService


class CorporationService(BaseService):
    def __init__(self, corporation_repository: CorporationRepository):
        super().__init__(corporation_repository)
        self.corporation_repository = corporation_repository

    async def get_corporation_by_name(self, db: AsyncSession, name: str) -> CorporationDomain:
        entity = await self.corporation_repository.find_by_name(db, name)
        if not entity:
            raise CorporationNotFoundException()
        return entity_to_domain(entity)

    async def create_corporation(
        self,
        db: AsyncSession,
        request: CorporationCreateRequestDto,
        admin_email: str,
        admin_password: str,
        user_service: UserService
    ) -> CorporationDomain:
        # 이름 중복 체크
        existing = await self.corporation_repository.find_by_name(db, request.name)
        if existing and request.id != existing.id:
            raise CorporationNameDuplicateException()

        # 기업 저장
        entity: CorporationEntity = domain_to_entity(request)
        created = await self.corporation_repository.save(db, entity)
        await db.flush()  # ID 확보용
        await db.refresh(created)

        # 관리자 유저 생성
        admin_domain = UserDomain(
            email=admin_email,
            password=admin_password,
            role=UserRole.ADMIN,
            corporation_id=created.id,
            point=0
        )
        await user_service.create_user(db, admin_domain)
        await db.commit()
        return entity_to_domain(created)

    async def get_corporation_by_id(self, db: AsyncSession, corporation_id: int) -> CorporationDomain:
        entity: CorporationEntity = await self.corporation_repository.find_by_id(db, corporation_id)
        if not entity:
            raise CorporationNotFoundException()

        # 만료일 확인 후 FREE 전환
        if entity.plan == "PAID" and entity.plan_expire_at and entity.plan_expire_at < datetime.utcnow():
            entity.plan = "FREE"
            await db.commit()
            await db.refresh(entity)

        return entity_to_domain(entity)

    async def get_all_corporations(self, db: AsyncSession) -> list[CorporationDomain]:
        entities = await self.corporation_repository.find_all(db)
        return [entity_to_domain(e) for e in entities]

    async def update_corporation(self, db: AsyncSession, corporation_id: int, request: CorporationUpdateRequestDto) -> CorporationDomain:

        update_dict = request.model_dump(exclude_unset=True)
        # 이름 중복 검사
        if "name" in update_dict:
            existing = await self.corporation_repository.find_by_name(db, update_dict["name"])
            if existing and existing.id != corporation_id:
                raise CorporationNameDuplicateException()

        # 업데이트
        entity: CorporationEntity = await self.corporation_repository.update(
            db,
            corporation_id,
            **update_dict
        )
        if not entity:
            raise CorporationNotFoundException()

        await db.commit()
        await db.refresh(entity)

        return entity_to_domain(entity)

    async def expire_outdated_paid_plans(self, db: AsyncSession) -> None:
        now = datetime.utcnow()
        corporations = await self.corporation_repository.find_expired_paid_plans(db, now)

        for corp in corporations:
            if corp.plan != CorporationPlan.FREE:
                corp.plan = CorporationPlan.FREE
                corp.plan_expire_at = None
                db.add(corp)

        await db.commit()

    async def delete_corporation(self, db: AsyncSession, corporation_id: int) -> None:
        # 삭제 전 엔티티 먼저 조회
        entity = await self.corporation_repository.find_by_id(db, corporation_id)
        if not entity:
            raise CorporationNotFoundException()

        # 삭제 수행
        await self.corporation_repository.soft_delete_by_id(db, corporation_id)
        await db.commit()
        await db.refresh(entity)

        return entity_to_domain(entity)
