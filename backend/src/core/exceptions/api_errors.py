from core.const.secrets import CODES


class ApiException(Exception):
    """Base API exception"""

    def __init__(self, code, *args, **kwargs):
        self.code = code
        self.rollback = kwargs.pop('rollback', True)
        super().__init__(*args)


class ApiError(ApiException):
    """Default API error"""

    def __init__(self, *args, **kwargs):
        super().__init__(CODES.API_ERROR, *args, **kwargs)


class HttpStatusError(Exception):
    """HTTP status error"""

    def __init__(self, status_code: int, *args):
        self.status_code = status_code
        super().__init__(*args)


class ParamError(ApiException):
    """Invalid parameter error"""

    def __init__(self, *args, **kwargs):
        super().__init__(CODES.PARAMETER_INVALID_TYPE, *args, **kwargs)


class ApiNotImplemented(ApiException):
    """API not implemented"""

    def __init__(self, *args, **kwargs):
        super().__init__(CODES.NOT_IMPLEMENTED, *args, **kwargs)


class MaxRetryError(Exception):
    """Maximum retry count exceeded"""
    pass
