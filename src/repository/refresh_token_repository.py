from src.repository.base_repository import BaseRepository
from src.entity.refresh_token_entity import RefreshTokenEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete


class RefreshTokenRepository(BaseRepository[RefreshTokenEntity]):
    """
    RefreshTokenEntity 전용 리포지토리.
    기본 CRUD는 BaseRepository에서 제공되며,
    도메인 특화 메서드를 여기에 정의합니다.
    """

    def __init__(self):
        super().__init__(RefreshTokenEntity)

    async def find_by_user_id(self, db: AsyncSession, user_id: int) -> RefreshTokenEntity | None:
        stmt = select(RefreshTokenEntity).where(RefreshTokenEntity.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def delete_by_user_id(self, db: AsyncSession, user_id: int):
        stmt = delete(RefreshTokenEntity).where(RefreshTokenEntity.user_id == user_id)
        await db.execute(stmt)
