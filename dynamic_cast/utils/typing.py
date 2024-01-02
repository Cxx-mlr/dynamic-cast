from typing import TypeVar
from typing import Any

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")
ARGUMENT = TypeVar("ARGUMENT", bound=Any)
ANNOTATION = TypeVar("ANNOTATION", bound=type)