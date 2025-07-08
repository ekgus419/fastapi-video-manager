from pydantic import BaseModel, Field, EmailStr


class LoginRequestDto(BaseModel):
    email: EmailStr = Field(..., description="이메일 (로그인 아이디)")
    password: str = Field(..., description="비밀번호")
