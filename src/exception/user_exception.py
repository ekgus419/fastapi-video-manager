from src.exception.base_exception import BaseAppException


class UserNotFoundException(BaseAppException):
    def __init__(self):
        super().__init__("유저를 찾을 수 없습니다.", status_code=404)

class InvalidAuthenticationException(BaseAppException):
    def __init__(self):
        super().__init__("유효하지 않은 인증 정보입니다.", status_code=401)

class InvalidCredentialsException(BaseAppException):
    def __init__(self):
        super().__init__("이메일 또는 비밀번호가 잘못되었습니다.", status_code=401)

class UserAlreadyExistsException(BaseAppException):
    def __init__(self):
        super().__init__("같은 기업 내에 이미 존재하는 이메일입니다.", status_code=409)

class PermissionUpdateDeniedException(BaseAppException):
    def __init__(self):
        super().__init__("해당 유저를 수정할 권한이 없습니다.", status_code=403)

class PermissionDeleteDeniedException(BaseAppException):
    def __init__(self):
        super().__init__("해당 유저를 삭제할 권한이 없습니다.", status_code=403)

class PermissionRestoreDeniedException(BaseAppException):
    def __init__(self):
        super().__init__("유료 플랜만 복구할 수 있습니다.", status_code=403)

class UserUnauthorizedException(BaseAppException):
    def __init__(self):
        super().__init__("권한이 없습니다.", status_code=403)

class AdminPrivilegesRequiredException(BaseAppException):
    def __init__(self):
        super().__init__("관리자 권한이 필요합니다.", status_code=403)

class GuestPrivilegesRequiredException(BaseAppException):
    def __init__(self):
        super().__init__("게스트 권한이 필요합니다.", status_code=403)