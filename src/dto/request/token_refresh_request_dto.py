from pydantic import BaseModel, Field


class RefreshRequestDto(BaseModel):
    refresh_token: str = Field(..., description="리프레시 토큰")

class RefreshTokenCreateRequestDto(BaseModel):
    user_id: int = Field(..., description="유저 ID")

class RefreshTokenUpdateRequestDto(BaseModel):
    token: str = Field(..., description="갱신된 토큰")
