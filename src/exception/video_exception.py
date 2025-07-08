from src.exception.base_exception import BaseAppException

class VideoNotFoundException(BaseAppException):
    def __init__(self):
        super().__init__("영상을 찾을 수 없습니다.", status_code=404)

class VideoAlreadyDeletedException(BaseAppException):
    def __init__(self):
        super().__init__("이미 삭제된 영상입니다.", status_code=400)

class VideoRestoreNotAllowedException(BaseAppException):
    def __init__(self):
        super().__init__("영상 복구는 유료 플랜에서만 가능합니다.", status_code=403)

class VideoStreamingFailedException(BaseAppException):
    def __init__(self):
        super().__init__("영상 스트리밍에 실패하였습니다.", status_code=502)