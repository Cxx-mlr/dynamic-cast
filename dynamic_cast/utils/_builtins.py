import importlib
import inspect

from ._typing import ANNOTATION

_builtins_members = dict(inspect.getmembers(importlib.import_module("builtins"))).values()

def _is_builtin(annotation: ANNOTATION) -> bool:
    return annotation in _builtins_members