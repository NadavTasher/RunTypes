import collections


def TypedTuple(name, fields):
    # Create namedtuple classtype
    original_class = collections.namedtuple(name, [key for key, _ in fields])

    # Create the subclass from the original class
    class modified_class(original_class):

        def __new__(cls, *args, **kwargs):
            # Initialize namedtuple with values
            self = original_class.__new__(cls, *args, **kwargs)

            # Type-check and replace
            self = self._replace(**{key: value_type(getattr(self, key)) for key, value_type in fields})

            # Return the new tuple
            return self

    # Replace the name with the original name
    modified_class.__name__ = name

    # Return the modified class
    return modified_class


# Create lower-case name for ease-of-use
typedtuple = TypedTuple
