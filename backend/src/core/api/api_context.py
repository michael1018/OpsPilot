from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import FrozenSet, Optional, Dict, Any


API_CONTEXT: ContextVar["ApiContext"] = ContextVar("API_CONTEXT")


@dataclass
class ApiContext:
    """
    Represents the request-scoped API context.

    ⚠️ Do NOT access this class directly.
    Always use ApiContext.current() to retrieve the active context.
    """

    # Context management
    scoped_key: Optional[str] = None
    scoped_token: Any = None

    # Authentication / identity
    auth: bool = False
    user_id: Optional[str] = None
    username: Optional[str] = None
    is_superuser: bool = False
    is_apiuser: bool = False

    # Security credentials
    token: Optional[str] = None
    secret: Optional[str] = None
    gac_secret: Optional[str] = None
    gac: Optional[str] = None

    # API metadata
    apiname: Optional[str] = None
    apimethod: Optional[str] = None
    descriptor: Any = None

    # Organization / permission
    dept_id: Optional[str] = None
    dept_code: Optional[str] = None
    role_codes: Optional[FrozenSet[str]] = None
    permission_codes: Optional[FrozenSet[str]] = None
    platforms: Optional[FrozenSet[str]] = None

    # Request information
    referer: Optional[str] = None
    remote_addr: Optional[str] = None
    x_forwarded_for: Optional[str] = None
    user_agent: Optional[str] = None
    platform: Optional[str] = None
    host: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None

    # Runtime objects
    session: Any = None
    params: Any = None
    kwargs: Optional[Dict[str, Any]] = field(default_factory=dict)

    # Response state
    response: bool = True

    # ------------------------------------------------------------------
    # Context helpers
    # ------------------------------------------------------------------

    @staticmethod
    def current() -> Optional["ApiContext"]:
        """
        Get the current request API context.

        :return: ApiContext or None if not initialized
        """
        return API_CONTEXT.get(None)

    @staticmethod
    def create(context: Optional["ApiContext"] = None) -> "ApiContext":
        """
        Create and bind a new ApiContext to the current execution scope.

        ⚠️ Use with caution. If you are unsure, do NOT call this manually.

        :param context: Optional existing ApiContext
        :return: ApiContext
        """
        if context is None:
            context = ApiContext()

        context.scoped_token = API_CONTEXT.set(context)
        return context
