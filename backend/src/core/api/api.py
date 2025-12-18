# core/api/api.py

from typing import Callable, Any
from core.api.api_core import ApiCore

class Api:
    _instance = None  # Singleton instance

    def __init__(self, api_core: ApiCore = None):
        if api_core is None:
            api_core = ApiCore()
        self._api_core = api_core

    @classmethod
    def get_instance(cls) -> "Api":
        """
        Get the singleton Api instance.
        If not created yet, create one.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def route(self, name: str = None, method: str = "GET", **kwargs):
        """
        Decorator to register a function as an API endpoint.
        """
        def decorator(func: Callable):
            api_name = name or func.__name__

            # Always store 'func' key explicitly
            descriptor = {"func": func, "method": method}
            descriptor.update(kwargs)  # add other optional info

            self._api_core.register_descriptor(api_name, descriptor)
            return func
        return decorator

    def get(self, name: str = None, **kwargs):
        return self.route(name=name, method="GET", **kwargs)

    def post(self, name: str = None, **kwargs):
        return self.route(name=name, method="POST", **kwargs)

    def put(self, name: str = None, **kwargs):
        return self.route(name=name, method="PUT", **kwargs)

    def delete(self, name: str = None, **kwargs):
        return self.route(name=name, method="DELETE", **kwargs)
