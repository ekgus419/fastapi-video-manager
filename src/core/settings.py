from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 환경 구분
    APP_ENV: str = "development"

    # DB 설정 (PostgreSQL)
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "lumanlab_db"

    # JWT
    JWT_SECRET: str = "your_secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRE_MINUTES: int = 10080   # 1주일
    JWT_REFRESH_EXPIRE_MINUTES: int = 40320  # 4주

    class Config:
        env_file = "src/env/.env.dev"

settings = Settings()
