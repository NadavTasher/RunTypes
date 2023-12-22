import functools
import collections


def typedtuple(name, fields):
    # Create namedtuple classtype
    namedtuple = collections.namedtuple(name, [key for key, _ in fields])

    # Fetch the original __new__ function
    original_constructor = namedtuple.__new__

    # Create __new__ function
    @functools.wraps(original_constructor)
    def __new__(cls, *args, **kwargs):
        # Initialize namedtuple with values
        self = original_constructor(cls, *args, **kwargs)

        # Type-check and replace
        self = self._replace(**{key: value_type(getattr(self, key)) for key, value_type in fields})

        # Return the new tuple
        return self

    # Replace the __new__ function
    namedtuple.__new__ = __new__

    # Return the namedtuple class
    return namedtuple
