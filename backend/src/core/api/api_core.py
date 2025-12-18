# core/api/api_core.py

from typing import Dict, Any

class ApiCore:
    def __init__(self):
        self._api_registry: Dict[str, Dict[str, Any]] = {}

    def register_descriptor(self, api_name: str, descriptor: Dict[str, Any]):
        """
        Register a descriptor dict for an API endpoint.
        """
        if "func" not in descriptor or not callable(descriptor["func"]):
            raise ValueError(f"Descriptor for {api_name} must have a callable 'func'")
        self._api_registry[api_name] = descriptor

    def get_registry(self):
        return self._api_registry
