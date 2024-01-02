from typing import Any, overload, Iterable, Sequence, MutableSequence, get_origin, Awaitable, Callable, OrderedDict
from collections.abc import Callable; from collections import OrderedDict

from types import MappingProxyType, UnionType
import functools
import inspect
from itertools import zip_longest

from .utils.typing import *

@overload
def async_cast(func_: Callable[P, Awaitable[R]], *, ret_value_error: Any | None=None)\
    -> Callable[..., Awaitable[R]]: ...

@overload
def async_cast(func_: None = None, *, ret_value_error: Any | None=None)\
    -> Callable[[Callable[P, Awaitable[R]]], Callable[..., Awaitable[R]]]: ...

def async_cast(func_: Callable[P, Awaitable[R]] | None = None, *, ret_value_error: Any | None=None)\
    -> Callable[..., Awaitable[R]] | Callable[[Callable[P, Awaitable[R]]], Callable[..., Awaitable[R]]]:
    async def async_cast_impl_(argument: ARGUMENT, annotation: ANNOTATION) -> Awaitable[ANNOTATION]:
        if annotation in (inspect.Parameter.empty, inspect.Signature.empty, Any):
            return argument
        elif isinstance(argument, str) and annotation is int:
            return await async_cast_impl_(
                await async_cast_impl_(argument, float),
                int
            )
        elif (origin := get_origin(annotation)) is not None:
            if origin is dict:
                key_type, value_type = getattr(annotation, "__args__", (Any, Any))
                return await async_cast_impl_(
                    {await async_cast_impl_(key, key_type): await async_cast_impl_(value, value_type) for key, value in argument.items()},
                    origin
                )
            elif issubclass(origin, Iterable):
                if issubclass(origin, MutableSequence):
                    value_type = getattr(annotation, "__args__", [lambda _: _])[0]
                    return await async_cast_impl_(
                        (await async_cast_impl_(arg, value_type) for arg in argument),
                        origin
                    )
                elif issubclass(origin, Sequence):
                    value_types = getattr(annotation, "__args__", [])
                    if len(value_types) == 1:
                        return await async_cast_impl_(
                            (
                                await async_cast_impl_(
                                    arg, value_type
                                )
                                for arg, value_type in zip_longest(
                                    argument, value_types, fillvalue=value_types[0]
                                )
                            ),
                            origin
                        )
                    else:
                        return await async_cast_impl_(
                            (
                                await async_cast_impl_(
                                    arg, value_type
                                )
                                for arg, value_type in zip(
                                    argument, value_types
                                )
                            ),
                            origin
                        )
            elif origin is UnionType:
                for element_type in (args := getattr(annotation, "__args__", ())):
                    try:
                        value = await async_cast_impl_(argument, element_type)
                    except ValueError:
                        continue
                    else:
                        return value
                if ret_value_error is not None:
                    return ret_value_error
                else:
                    conversion_type = "string" if isinstance(argument, str) else getattr(type(argument), '__name__', type(argument))
                    argument_repr = f"{argument!r}"
                    error_message = "".join(
                        f"\ncould not convert {conversion_type} to {getattr(arg, '__name__', arg)}: {argument_repr}" for arg in args
                    )
                    raise ValueError(error_message)
        else:
            try:
                value = annotation(argument)
            except ValueError:
                if ret_value_error is not None:
                    return ret_value_error
                else:
                    raise
            else:
                return value
    def decorator_async_cast(func: Callable[P, Awaitable[R]]) -> Callable[..., Awaitable[R]]:
        @functools.wraps(func)
        async def wrapper_async_cast(*args: Any, **kwargs: Any) -> R:
            signature: inspect.Signature = inspect.signature(func)
            parameters: MappingProxyType[str, inspect.Parameter] = signature.parameters
            bind: inspect.BoundArguments = signature.bind(*args, **kwargs)
            arguments: OrderedDict[str, Any] = bind.arguments
            args_f = list(); kwargs_f = dict()
            for pname, argument in arguments.items():
                parameter: inspect.Parameter = parameters[pname]
                annotation: type = parameter.annotation
                argument = await async_cast_impl_(argument, annotation)
                if parameter.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
                    args_f.append(argument)
                elif parameter.kind == inspect.Parameter.VAR_POSITIONAL:
                    args_f.extend(argument)
                elif parameter.kind in (inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.VAR_KEYWORD):
                    kwargs_f.update({pname: argument})
            return await async_cast_impl_(await func(*args_f, **kwargs_f), signature.return_annotation)
        return wrapper_async_cast
    if func_ is None:
        return decorator_async_cast
    else:
        return decorator_async_cast(func_)