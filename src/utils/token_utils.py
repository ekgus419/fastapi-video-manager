
from src.core.settings import settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db_session
from src.exception.user_exception import GuestPrivilegesRequiredException, AdminPrivilegesRequiredException, \
    InvalidAuthenticationException
from src.service.user_service import UserService
from src.domain.user_domain import UserDomain
from src.config.dependency_registry import get_user_service

bearer_scheme = HTTPBearer()

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service)
) -> UserDomain:
    try:
        # 토큰 문자열 추출
        token_str = token.credentials
        payload = jwt.decode(token_str, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise InvalidAuthenticationException()
    except JWTError:
        raise InvalidAuthenticationException()

    user = await user_service.get_by_id(db, int(user_id))

    if user is None:
        raise InvalidAuthenticationException()
    return user

async def get_current_active_admin(
    current_user: UserDomain = Depends(get_current_user)
) -> UserDomain:
    if current_user.role != "admin":
        raise AdminPrivilegesRequiredException()
    return current_user

async def get_current_active_guest(
    current_user: UserDomain = Depends(get_current_user)
) -> UserDomain:
    if current_user.role != "guest":
        raise GuestPrivilegesRequiredException()
    return current_user
