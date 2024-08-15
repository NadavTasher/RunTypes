def _assert(_condition, _error):
    # Check the value and raise accordingly
    if not _condition:
        raise TypeError(_error)


def _assert_istype(_value, _type):
    # Check the instance
    _assert(type(_value) == _type, f"Value is not of type {_type.__name__}")


def _assert_isinstance(_value, _type):
    # Check the instance
    _assert(isinstance(_value, _type), f"Value is not an instance of {_type}")