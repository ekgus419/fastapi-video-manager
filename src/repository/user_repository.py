from pydantic import EmailStr

from src.repository.base_repository import BaseRepository
from src.entity.user_entity import UserEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete


class UserRepository(BaseRepository[UserEntity]):
    """
    UserEntity 전용 리포지토리.
    기본 CRUD는 BaseRepository에서 제공되며,
    도메인 특화 메서드를 여기에 정의합니다.
    """

    def __init__(self):
        super().__init__(UserEntity)

    async def find_by_email(self, db: AsyncSession, email: EmailStr) -> UserEntity | None:
        stmt = select(UserEntity).where(UserEntity.email == email, UserEntity.deleted_at.is_(None))
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_email_and_corp(self, db: AsyncSession, email: str, corporation_id: int) -> UserEntity | None:
        stmt = select(UserEntity).where(
            UserEntity.email == email,
            UserEntity.corporation_id == corporation_id,
            UserEntity.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        return result.scalars().first()
