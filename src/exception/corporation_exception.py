from src.exception.base_exception import BaseAppException

class CorporationNotFoundException(BaseAppException):
    def __init__(self):
        super().__init__("기업을 찾을 수 없습니다.", status_code=404)

class CorporationNameDuplicateException(BaseAppException):
    def __init__(self):
        super().__init__("이미 존재하는 기업명입니다.", status_code=400)

class CorporationPlanUnauthorizedException(BaseAppException):
    def __init__(self):
        super().__init__("현재 플랜에서 사용할 수 없는 기능입니다.", status_code=403)
