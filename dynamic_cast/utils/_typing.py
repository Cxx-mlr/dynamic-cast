from typing import TypeVar
from typing import Any
import sys

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")
VALUE = TypeVar("VALUE")
ANNOTATION = TypeVar("ANNOTATION", bound=type)