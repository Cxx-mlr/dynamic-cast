from typing import Any, Iterable, Union, Optional, Callable, get_origin, get_args, overload
from collections import OrderedDict

from types import MappingProxyType

import functools
import inspect

from .utils.typing import *

def _is_callable(function: Any, *args: Any, **kwargs: Any) -> bool:
    try:
        inspect.signature(function).bind(*args, **kwargs)
    except Exception:
        return False
    else:
        return True

@overload
def dynamic_cast(func_: Callable[P, R]) -> Callable[..., R]: ...

@overload
def dynamic_cast(func_: None = None) -> Callable[[Callable[P, R]], Callable[..., R]]: ...

def dynamic_cast(func_: Optional[Callable[P, R]] = None) -> Union[
    Callable[..., R],
    Callable[[Callable[P, R]], Callable[..., R]]
]:
    @overload
    def dynamic_cast_impl(value: Any, annotation: None) -> None: ...

    @overload
    def dynamic_cast_impl(value: Any, annotation: ANNOTATION) -> ANNOTATION: ...

    @overload
    def dynamic_cast_impl(value: VALUE, annotation: Any) -> VALUE: ...

    def dynamic_cast_impl(value, annotation):
        if annotation is None:
            return None
        elif annotation in (inspect.Parameter.empty, inspect.Signature.empty, Any):
            return value
        elif annotation is int and isinstance(value, str):
            return dynamic_cast_impl(
                dynamic_cast_impl(value, float), int
            )
        elif (__origin__ := get_origin(annotation)) is not None:
            if issubclass(__origin__, Mapping):
                __args__ = get_args(annotation) or (Any, Any)
                key_type, value_type = __args__

                return dynamic_cast_impl(
                    {dynamic_cast_impl(key, key_type):dynamic_cast_impl(value, value_type) for key, value in value.items()},
                    __origin__
                )
            elif issubclass(__origin__, Iterable):
                __args__ = get_args(annotation) or ()
                if len(__args__) == 1 or len(__args__) == 2 and __args__[1] is Ellipsis:
                    return dynamic_cast_impl(
                        (dynamic_cast_impl(i, __args__[0]) for i in value),
                        __origin__
                    )
                else:
                    offset = len(value)
                    remaining_annotations = __args__[offset:]
                    default_constructed = [x() for x in remaining_annotations]

                    merged_values = list(value) + default_constructed
                    return dynamic_cast_impl(
                        (dynamic_cast_impl(i, value_type) for i, value_type in zip(merged_values, __args__)),
                        __origin__
                    )
            else:
                return None
        elif _is_callable(getattr(annotation, "__init__"), value) or _is_callable(annotation, value):
            return annotation(value)
        else:
            return value
    def decorator_dynamic_cast(func: Callable[P, R]) -> Callable[..., R]:
        @functools.wraps(func)
        def wrapper_dynamic_cast(*args: Any, **kwargs: Any) -> R:
            signature: inspect.Signature = inspect.signature(func)
            parameters: MappingProxyType[str, inspect.Parameter] = signature.parameters
            bind: inspect.BoundArguments = signature.bind(*args, **kwargs)
            arguments: OrderedDict[str, Any] = bind.arguments
            args_f = list(); kwargs_f = dict()
            for pname, value in arguments.items():
                parameter: inspect.Parameter = parameters[pname]
                annotation: type = parameter.annotation
                value = dynamic_cast_impl(value, annotation)
                if parameter.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
                    args_f.append(value)
                elif parameter.kind == inspect.Parameter.VAR_POSITIONAL:
                    args_f.extend(value)
                elif parameter.kind in (inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.VAR_KEYWORD):
                    kwargs_f[pname] = value
            ret = func(*args_f, **kwargs_f)
            return dynamic_cast_impl(ret, signature.return_annotation)
        return wrapper_dynamic_cast
    if func_ is None:
        return decorator_dynamic_cast
    else:
        return decorator_dynamic_cast(func_)