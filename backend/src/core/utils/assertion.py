# core/utils/assertion.py

import inspect
from typing import Any

from core.exceptions import ParamError


class Assert:
    """
    Assertion helpers.
    Raise ParamError when validation fails.
    """

    @staticmethod
    def is_not_null(value: Any, message: str):
        if value is None:
            raise ParamError(message)

    @staticmethod
    def is_not_dict(value: Any, message: str, nullable: bool = False):
        if nullable and value is None:
            return
        if not isinstance(value, dict):
            raise ParamError(message)

    @staticmethod
    def is_not_list(value: Any, message: str, nullable: bool = False):
        if nullable and value is None:
            return
        if not isinstance(value, list):
            raise ParamError(message)

    @staticmethod
    def is_not_int(value: Any, message: str, nullable: bool = False):
        if nullable and value is None:
            return
        if not isinstance(value, int):
            raise ParamError(message)

    @staticmethod
    def is_not_bool(value: Any, message: str, nullable: bool = False):
        if nullable and value is None:
            return
        if not isinstance(value, bool):
            raise ParamError(message)

    @staticmethod
    def is_not_function(value: Any, message: str, nullable: bool = False):
        if nullable and value is None:
            return
        if not inspect.isfunction(value):
            raise ParamError(message)
