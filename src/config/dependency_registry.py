from fastapi import Depends
from src.repository.user_repository import UserRepository
from src.service.user_service import UserService

from src.repository.corporation_repository import CorporationRepository
from src.service.corporation_service import CorporationService

from src.repository.video_repository import VideoRepository
from src.service.video_service import VideoService

from src.repository.video_view_log_repository import VideoViewLogRepository
from src.service.video_view_log_service import VideoViewLogService

from src.repository.refresh_token_repository import RefreshTokenRepository
from src.service.refresh_token_service import RefreshTokenService


# User
def get_user_repository() -> UserRepository:
    return UserRepository()

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)



# Corporation
def get_corporation_repository() -> CorporationRepository:
    return CorporationRepository()

def get_corporation_service() -> CorporationService:
    repo = get_corporation_repository()
    return CorporationService(repo)



# Video
def get_video_repository() -> VideoRepository:
    return VideoRepository()

def get_video_service(repo: VideoRepository = Depends(get_video_repository)) -> VideoService:
    return VideoService(repo)



# Video View Log
def get_video_view_log_repository() -> VideoViewLogRepository:
    return VideoViewLogRepository()

def get_video_view_log_service(repo: VideoViewLogRepository = Depends(get_video_view_log_repository)) -> VideoViewLogService:
    return VideoViewLogService(repo)



# Refresh Token
def get_refresh_token_repository() -> RefreshTokenRepository:
    return RefreshTokenRepository()

def get_refresh_token_service(repo: RefreshTokenRepository = Depends(get_refresh_token_repository)) -> RefreshTokenService:
    return RefreshTokenService(repo)
