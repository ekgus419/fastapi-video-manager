from typing import Optional

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user_domain import UserDomain
from src.dto.request.user_request_dto import UserUpdateRequestDto
from src.enums.user_enums import UserRole
from src.exception.user_exception import UserNotFoundException, UserAlreadyExistsException, \
    PermissionUpdateDeniedException, PermissionDeleteDeniedException
from src.mapper.user_mapper import entity_to_domain, domain_to_entity
from src.service.base_service import BaseService
from src.repository.user_repository import UserRepository
from src.entity.user_entity import UserEntity
from src.utils.password_utils import hash_password, verify_password


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)
        self.user_repository = user_repository

    async def get_user_by_email(self, db: AsyncSession, email: EmailStr) -> UserDomain:
        entity = await self.user_repository.find_by_email(db, email)
        if not entity:
            raise UserNotFoundException()
        return entity_to_domain(entity)

    async def verify_credentials(self, db: AsyncSession, email: EmailStr, password: str) -> Optional[UserDomain]:
        user = await self.user_repository.find_by_email(db, email)
        import bcrypt
        if user and bcrypt.checkpw(password.encode("utf-8"), str(user.password).encode("utf-8")):
            return user
        return None

    async def create_user(self, db: AsyncSession, domain: UserDomain) -> UserDomain:
        # 중복 확인(기업이 다르다면 중복 허용)
        existing = await self.user_repository.find_by_email_and_corp(
            db, domain.email, domain.corporation_id
        )

        if existing:
            raise UserAlreadyExistsException()

        # 비밀번호 암호화
        domain.password = hash_password(domain.password)

        entity: UserEntity = domain_to_entity(domain)
        created = await self.user_repository.save(db, entity)
        await db.commit()
        await db.refresh(created)
        return entity_to_domain(created)

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> UserDomain:
        entity: UserEntity = await self.user_repository.find_by_id(db, user_id)
        if not entity:
            raise UserNotFoundException()
        return entity_to_domain(entity)

    async def get_all_users(self, db: AsyncSession) -> list[UserDomain]:
        entities = await self.user_repository.find_all(db)
        return [entity_to_domain(e) for e in entities]

    async def update_user(
        self,
        db: AsyncSession,
        user_id: int,
        request: UserUpdateRequestDto,
        current_user: UserDomain
    ) -> UserDomain:
        target = await self.user_repository.find_by_id(db, user_id)
        if not target:
            raise UserNotFoundException()

        request = request.model_dump(exclude_unset=True)

        # 자기 자신이 아닌 경우
        if current_user.id != user_id:
            # 같은 기업이고 admin 권한이 아닌 경우
            if (
                    current_user.corporation_id != target.corporation_id
                    or current_user.role != UserRole.ADMIN
            ):
                raise PermissionUpdateDeniedException()

        # 비밀번호 변경 시 암호화
        if "password" in request and request["password"]:
            request["password"] = hash_password(request["password"])

        updated = await self.user_repository.update(db, user_id, **request)
        await db.commit()
        await db.refresh(updated)
        return entity_to_domain(updated)

    async def add_point(self, db: AsyncSession, user_id: int, point: int) -> None:
        user = await self.user_repository.find_by_id(db, user_id)
        if not user:
            raise UserNotFoundException()

        user.point += point
        await db.commit()
        await db.refresh(user)

    async def delete_user(
        self,
        db: AsyncSession,
        user_id: int,
        current_user: UserDomain
    ) -> None:
        target = await self.user_repository.find_by_id(db, user_id)
        if not target:
            raise UserNotFoundException()

        # 자기 자신이 아닌 경우
        if current_user.id != user_id:
            # 권한 조건 위반
            if (
                    current_user.corporation_id != target.corporation_id
                    or current_user.role != UserRole.ADMIN
            ):
                raise PermissionDeleteDeniedException()

        await self.user_repository.soft_delete_by_id(db, user_id)
        await db.commit()
