# core/__init__.py

"""
OpsPilot Core Package
--------------------
This package contains the core functionality of OpsPilot,
including API registration and server utilities.
"""

# Expose main modules for easy import
from core.api.api_core import ApiCore
from core.api.api import Api
from core.server.restful_server import RESTFulApiServer

# Optional: create a default global API instance
# This allows importing `from core import api` directly
api_core = ApiCore()
api = Api(api_core)

__all__ = [
    "ApiCore",
    "Api",
    "RESTFulApiServer",
    "api_core",
    "api",
]
