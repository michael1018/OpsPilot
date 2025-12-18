import json
from enum import Enum
from typing import Any, Callable, Dict, Optional


class ApiResponseType(Enum):
    STREAM = "stream"
    FILE = "file"
    FILE_STREAM = "file_stream"


class ApiResponse:
    """
    Standard API response wrapper for OpsPilot
    """

    def __init__(
        self,
        code: int = 0,
        data: Any = None,
        message: Optional[str] = None,
        total: Optional[int] = None,
        exts: Any = None,
        streaming_fn: Optional[Callable] = None,
        path: Optional[str] = None,
        filename: Optional[str] = None,
        type: Optional[ApiResponseType] = None,
        content_type: Optional[str] = None,
        rollback: bool = True,
        headers: Optional[Dict[str, str]] = None,
        status_code: int = 200,
        body: Optional[str] = None,
        **kwargs,
    ):
        """
        API response object

        :param code: Business status code (0 means success)
        :param data: Response payload (must be JSON serializable)
        :param message: Human-readable message
        :param total: Total count for paginated responses
        :param exts: Extra custom fields
        :param streaming_fn: Streaming response callable
        :param path: File path (for file responses)
        :param filename: Download filename
        :param type: ApiResponseType
        :param content_type: MIME type
        :param rollback: Whether transaction should rollback on error
        :param headers: HTTP headers
        :param status_code: HTTP status code
        :param body: Raw body (used when status_code > 300)
        """
        self.code = code
        self.data = data
        self.message = message
        self.total = total
        self.exts = exts
        self.streaming_fn = streaming_fn
        self.path = path
        self.filename = filename
        self.type = type
        self.content_type = content_type
        self.rollback = rollback
        self.headers = headers or {}
        self.status_code = status_code
        self.body = body
        self.kwargs = kwargs

    def to_json(self) -> Dict[str, Any]:
        """
        Convert response to JSON-serializable dict
        """
        if self.status_code >= 300:
            return self.body

        result = {"code": self.code}

        if self.message:
            result["message"] = self.message

        if self.data is not None:
            if isinstance(self.data, (list, dict, str, int, float, bool, tuple)):
                result["data"] = self.data
            else:
                raise TypeError(
                    f"Invalid data type for JSON serialization: {type(self.data)}"
                )

        if self.total is not None:
            result["total"] = self.total

        if self.exts is not None:
            result["exts"] = self.exts

        return result

    # ------------------------------
    # Factory methods
    # ------------------------------

    @staticmethod
    def success(
        data: Any = None,
        message: Optional[str] = None,
        total: Optional[int] = None,
        exts: Any = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> "ApiResponse":
        """
        Create a successful API response
        """
        return ApiResponse(
            code=0,
            data=data,
            message=message,
            total=total,
            exts=exts,
            headers=headers,
        )

    @staticmethod
    def error(
        code: int,
        message: Optional[str] = None,
        rollback: bool = True,
        headers: Optional[Dict[str, str]] = None,
        status_code: int = 200,
    ) -> "ApiResponse":
        """
        Create an error API response
        """
        return ApiResponse(
            code=code,
            message=message,
            rollback=rollback,
            headers=headers,
            status_code=status_code,
        )

    @staticmethod
    def stream(
        streaming_fn: Callable,
        content_type: str = "text/plain",
    ) -> "ApiResponse":
        """
        Create a streaming response
        """
        if not callable(streaming_fn):
            raise ValueError("streaming_fn must be callable")

        return ApiResponse(
            streaming_fn=streaming_fn,
            type=ApiResponseType.STREAM,
            content_type=content_type,
        )

    @staticmethod
    def file(
        path: str,
        content_type: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> "ApiResponse":
        """
        Create a small file response
        """
        if not path:
            raise ValueError("path is required")

        return ApiResponse(
            path=path,
            filename=filename,
            type=ApiResponseType.FILE,
            content_type=content_type,
        )

    @staticmethod
    def file_stream(
        path: str,
        content_type: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> "ApiResponse":
        """
        Create a large file streaming response
        """
        if not path:
            raise ValueError("path is required")

        return ApiResponse(
            path=path,
            filename=filename,
            type=ApiResponseType.FILE_STREAM,
            content_type=content_type,
        )

    def __str__(self) -> str:
        return json.dumps(self.to_json(), ensure_ascii=False)
