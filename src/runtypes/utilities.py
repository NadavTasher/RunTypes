def _assert(_condition, _error):
    # Check the value and raise accordingly
    if not _condition:
        raise TypeError(_error)


def _assert_istype(_value, _type):
    # Check the instance
    _assert(type(_value) == _type, "Value is not of type {0}".format(_type.__name__))


def _assert_isinstance(_value, _type):
    # Check the instance
    _assert(isinstance(_value, _type), "Value is not an instance of {0}".format(_type))