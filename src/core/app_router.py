from fastapi import FastAPI

from src.routers import (
    user_router,
    auth_router,
    corporation_router,
    video_router,
    video_view_log_router,
    refresh_token_router
)

def register_routers(app: FastAPI):
    """
    FastAPI 애플리케이션에 모든 라우터를 등록하는 메소드
    """
    # 인증 관련 API 라우터
    app.include_router(auth_router.router, prefix="/v1/auth", tags=["Auth"])
    # 사용자 관련 API 라우터
    app.include_router(user_router.router, prefix="/v1/users", tags=["User"])
    # 동영상 관련 API
    app.include_router(video_router.router, prefix="/v1/videos", tags=["Video"])
    # 기업 관련 API
    app.include_router(corporation_router.router,  prefix="/v1/corporations", tags=["Corporation"])
    # 동영상 시청 로그 관련 API
    app.include_router(video_view_log_router.router, prefix="/v1/view-logs", tags=["VideoViewLog"])
    # 리프레시 토큰 관련 API 라우터 등록 (access token 재발급 등)
    app.include_router(refresh_token_router.router, prefix="/v1/tokens", tags=["RefreshToken"])
