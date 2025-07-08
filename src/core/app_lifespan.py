from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.scheduler import start_plan_expiry_scheduler


# FastAPI 앱의 수명 주기를 관리하는 컨텍스트 매니저입니다.
# 앱이 시작될 때와 종료될 때 실행할 로직을 정의할 수 있습니다.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱이 시작될 때 실행되는 코드 (예: DB 연결, 초기화 작업 등)
    print("🚀 Application started 🚀")

    # 스케줄러 실행: 24시간마다 자동 갱신
    start_plan_expiry_scheduler()

    # yield 지점에서 앱이 실행되며, FastAPI는 이 상태로 유지됩니다.
    yield

    # 앱이 종료될 때 실행되는 코드 (예: 리소스 정리, 로그 처리 등)
    print("🛑 Application shutdown 🛑")
