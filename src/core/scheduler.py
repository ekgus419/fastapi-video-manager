from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from src.config.dependency_registry import get_corporation_service
from src.core.database import get_db_session

scheduler = AsyncIOScheduler()

def start_plan_expiry_scheduler():
    # 매일 00:00마다 실행
    scheduler.add_job(
        expire_outdated_plans_job,
        trigger=IntervalTrigger(hours=24),  # 또는 cron='0 0 * * *'
        next_run_time=datetime.utcnow()     # 시작 시 즉시 한 번 실행
    )
    scheduler.start()

async def expire_outdated_plans_job():
    print("⏰ [Scheduler] Checking expired plans...")
    # 유료 플랜의 만료 기한이 지난 기업들을 FREE 플랜으로 자동 전환합니다.
    async with get_db_session() as db:
        service = get_corporation_service()
        await service.expire_outdated_paid_plans(db)
