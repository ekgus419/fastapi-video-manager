from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.app_lifespan import lifespan
from src.core.app_router import register_routers
from src.exception.exception_handler import add_exception_handlers


def create_app() -> FastAPI:
    """
    FastAPI 애플리케이션 인스턴스를 생성하고
    주요 미들웨어, 예외 처리, 라우터, 수명주기 핸들러를 등록합니다.
    """
    app = FastAPI(
        title="LumanLab Backend",
        description="Video Management API",
        version="1.0.0",
        servers=[
            {"url": "http://localhost:80", "description": "Localhost over Nginx (port 80)"}
        ],
        lifespan=lifespan
    )

    # 예외 처리기 등록
    add_exception_handlers(app)

    # CORS 설정 (개발 단계에서는 전체 허용)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록
    register_routers(app)

    return app
