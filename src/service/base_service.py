from typing import TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.base_repository import BaseRepository
from src.entity.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseService(Generic[T]):
    """
    공통적인 서비스 로직을 제공하는 추상 클래스.
    모든 도메인 서비스는 이 클래스를 상속받아 기본 CRUD 기능을 재사용합니다.
    """

    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    async def get_by_id(self, db: AsyncSession, entity_id: int) -> T:
        entity = await self.repository.find_by_id(db, entity_id)
        if not entity:
            raise Exception(f"{self.__class__.__name__} - ID {entity_id} not found")
        return entity

    async def create(self, db: AsyncSession, entity: T) -> T:
        return await self.repository.save(db, entity)

    async def update(self, db: AsyncSession, entity_id: int, **kwargs) -> T:
        return await self.repository.update(db, entity_id, **kwargs)

    async def delete(self, db: AsyncSession, entity_id: int) -> bool:
        return await self.repository.delete_by_id(db, entity_id)

    async def soft_delete(self, db: AsyncSession, entity_id: int) -> T:
        return await self.repository.soft_delete_by_id(db, entity_id)

    async def exists_by_id(self, db: AsyncSession, entity_id: int) -> bool:
        return await self.repository.exists_by_id(db, entity_id)
