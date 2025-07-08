from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.domain.refreshtoken_domain import RefreshTokenDomain
from src.exception.refresh_token_exception import RefreshTokenNotFoundException
from src.mapper.refreshtoken_mapper import entity_to_domain, domain_to_entity
from src.service.base_service import BaseService
from src.repository.refresh_token_repository import RefreshTokenRepository
from src.entity.refresh_token_entity import RefreshTokenEntity
from src.utils.jwt_utils import create_refresh_token


class RefreshTokenService(BaseService):
    def __init__(self, refresh_token_repository: RefreshTokenRepository):
        super().__init__(refresh_token_repository)
        self.refresh_token_repository = refresh_token_repository

    async def get_token_by_user_id(self, db: AsyncSession, user_id: int) -> RefreshTokenDomain | None:
        entity = await self.refresh_token_repository.find_by_user_id(db, user_id)
        return entity_to_domain(entity) if entity else None

    async def delete_token_by_user_id(self, db: AsyncSession, user_id: int):
        await self.refresh_token_repository.delete_by_user_id(db, user_id)

    async def save_refresh_token(self, db: AsyncSession, user_id: int, token: str) -> None:
        domain = await self.refresh_token_repository.find_by_user_id(db, user_id)
        if domain:
            domain.token = token
        else:
            domain = RefreshTokenDomain(user_id=user_id, token=token)
            db.add(domain)
        await db.commit()

    async def get_by_user_id(self, db: AsyncSession, user_id: int) -> RefreshTokenDomain:
        entity = await self.refresh_token_repository.find_by_user_id(db, user_id)
        if not entity:
            raise RefreshTokenNotFoundException()
        return entity_to_domain(entity)

    async def create_token(self, db: AsyncSession, domain: RefreshTokenDomain) -> RefreshTokenDomain:
        entity: RefreshTokenEntity = RefreshTokenEntity(
            user_id=domain.user_id,
            token=create_refresh_token({"sub": str(domain.user_id)}),  # JWT 생성
            expires_at=datetime.utcnow() + timedelta(minutes=settings.JWT_REFRESH_EXPIRE_MINUTES)
        )
        saved = await self.refresh_token_repository.save(db, entity)
        await db.commit()
        await db.refresh(saved)
        return entity_to_domain(saved)