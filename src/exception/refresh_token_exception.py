from src.exception.base_exception import BaseAppException

class RefreshTokenNotFoundException(BaseAppException):
    def __init__(self):
        super().__init__("Refresh Token을 찾을 수 없습니다.", status_code=404)

class RefreshTokenExpiredException(BaseAppException):
    def __init__(self):
        super().__init__("Refresh Token이 만료되었습니다.", status_code=401)

class RefreshTokenDecodeException(BaseAppException):
    def __init__(self):
        super().__init__("Refresh token 해석에 실패하였습니다.", status_code=401)

class InvalidRefreshTokenException(BaseAppException):
    def __init__(self):
        super().__init__("유효하지 않은 Refresh Token입니다.", status_code=401)
