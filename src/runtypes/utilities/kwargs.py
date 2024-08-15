import functools


def kwargchecker(**types):

    # Create a decorator generator
    def generator(function):

        # Generate a decorator
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            # Loop over type arguments
            for key, value_type in types.items():
                # Make sure the kwarg value is an instance of the value type
                if not isinstance(kwargs.get(key), value_type):
                    raise TypeError(f"Argument {key!r} is not an instance of {value_type!r}")

            # Call the target function
            return function(*args, **kwargs)

        # Return the decorator
        return wrapper

    # Return the wrapper generator
    return generator
