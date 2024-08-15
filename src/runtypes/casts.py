from runtypes.types import Text
from runtypes.typecaster import typecaster
from runtypes.utilities import _assert, _assert_isinstance


@typecaster
def ListCast(value, item_type):
    # Make sure value is a list
    _assert_isinstance(value, list)

    # Loop over value and cast items
    return list(item_type(item) for item in value)


@typecaster
def DictCast(value, key_type, value_type):
    # Make sure value is a dictionary
    _assert_isinstance(value, dict)

    # Loop over value and cast items
    return dict({key_type(_key): value_type(_value) for _key, _value in value.items()})


@typecaster
def TupleCast(value, *item_types):



@typecaster



@typecaster
def CharsetCast(value, chars):
    # Make sure value is a string
    _assert_isinstance(value, Text)

    # Cast value to chars
    return "".join(char for char in value if char in chars)


# Initialize some charsets
IDCast = CharsetCast["abcdefghijklmnopqrstuvwxyz0123456789"]
BinaryCast = CharsetCast["01"]
DecimalCast = CharsetCast["0123456789"]
HexadecimalCast = CharsetCast["0123456789ABCDEFabcdef"]
