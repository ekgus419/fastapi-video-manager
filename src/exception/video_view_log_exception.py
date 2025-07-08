from src.exception.base_exception import BaseAppException

class VideoViewLogNotFoundException(BaseAppException):
    def __init__(self):
        super().__init__("영상 조회 이력을 찾을 수 없습니다.", status_code=404)
