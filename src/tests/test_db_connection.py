import asyncio
from sqlalchemy import text
import pytest
from src.core.database import engine


@pytest.mark.asyncio
async def test_db_connection():
    """
    PostgreSQL 연결 테스트 함수입니다.
    SELECT 1 쿼리를 실행하고 정상 응답이 나오면 연결 성공으로 간주합니다.
    python -m src.tests.test_db_connection
    """
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            assert result.scalar_one() == 1
            print("✅ PostgreSQL 연결 성공!")
    except Exception as e:
        print("❌ PostgreSQL 연결 실패:", e)


if __name__ == "__main__":
    asyncio.run(test_db_connection())
