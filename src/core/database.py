from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy.engine.url import URL
from src.core.settings import settings

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,           # SQL 쿼리 로그 출력
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
)

async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# FastAPI 의존성 주입용
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@asynccontextmanager
async def get_scheduler_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session
