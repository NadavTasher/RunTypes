import inspect
import functools

from runtypes.types import Any
from runtypes.utilities import _assert_isinstance


def hintcheck(function, args, kwargs):
    # Get the function signature
    signature = inspect.signature(function)

    # Create a dictionary with all parameters
    parameters = dict()

    # Loop over variable names and fetch the respective variable
    for index, (name, parameter) in enumerate(signature.parameters.items()):
        # Check whether the argument is provided via args
        if index < len(args):
            parameters[name] = args[index]
            continue

        # Check whether the argument is provided via kwargs
        if name in kwargs:
            parameters[name] = kwargs[name]
            continue

        # Check whether the argument is provided via defaults
        if parameter.default is not inspect._empty:
            parameters[name] = parameter.default
            continue

        # Argument was not provided!

    # Validate all types
    for name, value in parameters.items():
        # Fetch type annotation
        annotation = signature.parameters[name].annotation

        # If there is no annotation, continue
        if annotation is inspect._empty:
            continue

        # Make sure the type is correct
        if not isinstance(value, annotation):
            raise TypeError(f"Argument {name!r} is not an instance of {annotation!r}")


# Create a decorator generator
def hintchecker(function):

    # Generate a decorator
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        # Check the type hints
        hintcheck(function, args, kwargs)

        # Call the target function
        return function(*args, **kwargs)

    # Return the decorator
    return wrapper
