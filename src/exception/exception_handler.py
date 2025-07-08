from fastapi import Request
from fastapi.responses import JSONResponse
from src.dto.response.common_response_dto import CommonResponseDto
from src.exception.base_exception import BaseAppException


def add_exception_handlers(app):
    @app.exception_handler(BaseAppException)
    async def handle_custom_exception(request: Request, exc: BaseAppException):
        return JSONResponse(
            status_code=exc.status_code,
            content=CommonResponseDto(
                status="fail",
                message=exc.message,
                data=None
            ).model_dump()
        )

