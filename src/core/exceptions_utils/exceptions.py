class AppException(Exception):
    def __init__(self, status_code : int, detail : str):
        self.status_code = status_code
        self.detail = detail

class ResourceConflictError(AppException):
    def __init__(self, detail="Resource Conflict"):
        super().__init__(409, detail)

class BadRequestError(AppException):
    def __init__(self, detail="Bad Request"):
        super().__init__(400, detail)