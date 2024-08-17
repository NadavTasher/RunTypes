import typing
import inspect
import functools

from runtypes.types.basic import Any
from runtypes.runtype import _resolve_function_arguments


def _resolve_function_types(function: typing.Callable[..., typing.Any]) -> typing.Dict[str, type]:
    # Create a dictionary of types
    return {
        # Any as default, annotation if defined
        name: Any if parameter.annotation is inspect._empty else parameter.annotation
        # For all signature parameters
        for name, parameter in inspect.signature(function).parameters.items()
    }


def cast_type_hints(function: typing.Callable[..., typing.Any], args: typing.Sequence[typing.Any], kwargs: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    # Resolve function types and arguments
    types = _resolve_function_types(function)
    arguments = _resolve_function_arguments(function, args, kwargs)

    # Create a casted dictionary with all items
    return {
        # Cast the argument using the argument type
        argument_name: argument_type(arguments.get(argument_name))
        # For all provided types
        for argument_name, argument_type in types.items()
    }


def check_type_hints(function: typing.Callable[..., typing.Any], args: typing.Sequence[typing.Any], kwargs: typing.Dict[str, typing.Any]) -> None:
    # Resolve function types and arguments
    types = _resolve_function_types(function)
    arguments = _resolve_function_arguments(function, args, kwargs)

    # Loop over the provided types and check them
    for argument_name, argument_type in types.items():
        # Check the argument type
        if not isinstance(arguments.get(argument_name), argument_type):
            raise TypeError(f"Argument {argument_name!r} is not an instance of {argument_type!r}")


def typecast(function: typing.Callable[..., typing.Any]) -> typing.Callable[..., typing.Any]:

    @functools.wraps(function)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        # Check the type hints
        arguments = cast_type_hints(function, args, kwargs)

        # Call the target function
        return function(**arguments)

    # Return the decorator
    return wrapper


def typecheck(function: typing.Callable[..., typing.Any]) -> typing.Callable[..., typing.Any]:

    @functools.wraps(function)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        # Check the type hints
        check_type_hints(function, args, kwargs)

        # Call the target function
        return function(*args, **kwargs)

    # Return the decorator
    return wrapper
