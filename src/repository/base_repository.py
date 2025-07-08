from typing import TypeVar, Generic, Optional, Type, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, inspect
from sqlalchemy.sql.elements import ColumnElement
from src.entity.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):
    """
    공통적인 데이터 접근 로직을 제공하는 추상 클래스.
    모든 엔티티 리포지토리는 이 클래스를 상속받아 공통 기능을 재사용함.
    """

    def __init__(self, entity: Type[T]):
        """
        :param entity: ORM 모델 클래스 (Base를 상속해야 함)
        """
        self.entity = entity

        # 기본 키가 존재하는지 체크
        primary_keys = inspect(self.entity).primary_key
        if not primary_keys:
            raise ValueError(f"{self.entity.__name__} 모델에 기본 키가 없습니다.")

        # 기본 키 이름 → SQLAlchemy 컬럼 객체로 저장
        primary_key_name = primary_keys[0].name
        self.primary_key_column: ColumnElement = getattr(self.entity, primary_key_name)

    async def find_all(self, db: AsyncSession) -> Sequence[T]:
        stmt = select(self.entity).where(self.entity.deleted_at.is_(None))
        result = await db.execute(stmt)
        return result.scalars().all()

    async def find_by_id(self, db: AsyncSession, entity_id: int) -> Optional[T]:
        stmt = select(self.entity).where(
            self.primary_key_column == entity_id,
            self.entity.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def count_all(self, db: AsyncSession, filters: Optional[list] = None) -> int:
        stmt = select(func.count()).select_from(self.entity).where(self.entity.deleted_at.is_(None))
        if filters:
            for f in filters:
                stmt = stmt.where(f)
        result = await db.execute(stmt)
        return result.scalar_one()

    async def save(self, db: AsyncSession, entity: T) -> T:
        db.add(entity)
        await db.flush()
        return entity

    async def update(self, db: AsyncSession, entity_id: int, **kwargs) -> Optional[T]:
        stmt = (
            update(self.entity)
            .where(self.primary_key_column == entity_id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(stmt)
        return await self.find_by_id(db, entity_id)

    async def delete_by_id(self, db: AsyncSession, entity_id: int) -> bool:
        stmt = delete(self.entity).where(self.primary_key_column == entity_id)
        result = await db.execute(stmt)
        return result.rowcount > 0

    async def soft_delete_by_id(self, db: AsyncSession, entity_id: int) -> Optional[T]:
        stmt = (
            update(self.entity)
            .where(self.primary_key_column == entity_id)
            .values(deleted_at=func.now())
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(stmt)
        return await self.find_by_id(db, entity_id)

    async def exists_by_id(self, db: AsyncSession, entity_id: int) -> bool:
        stmt = select(func.count()).select_from(self.entity).where(
            self.primary_key_column == entity_id,
            self.entity.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        return result.scalar_one() > 0
