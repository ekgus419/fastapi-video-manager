from pydantic import BaseModel, Field
from typing import Generic, Optional, TypeVar

DataT = TypeVar("DataT")

class CommonResponseDto(BaseModel, Generic[DataT]):
    """
    모든 API 응답의 공통 형식
    """
    status: str = Field(..., description="응답 상태 (success, error, fail)")
    data: Optional[DataT] = Field(None, description="응답 데이터")
    message: Optional[str] = Field(None, description="응답 메시지 또는 에러 설명")
