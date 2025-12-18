# core/api/__init__.py

"""
OpsPilot API Package
-------------------
Contains core API registration and server utilities.
"""

from core.api.api_core import ApiCore
from core.api.api import Api

# Default global instances for quick registration
api_core = ApiCore()
api = Api(api_core)

__all__ = [
    "ApiCore",
    "Api",
    "api_core",
    "api",
]
