import functools


def kwargchecker(**types):

    # Create a decorator generator
    def generator(function):

        # Generate a decorator
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            # Loop over type arguments
            for name, typechecker in types.items():
                # Execute type-check and update the value
                kwargs[name] = typechecker(kwargs.get(name))

            # Call the target function
            return function(*args, **kwargs)

        # Return the decorator
        return wrapper

    # Return the wrapper generator
    return generator
