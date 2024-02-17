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
    # Make sure value is a tuple
    _assert_isinstance(value, tuple)

    # Make sure value is of length
    _assert(len(value) == len(item_types), "Value length does not match types")

    # Check all item types
    return tuple(item_type(item) for item, item_type in zip(value, item_types))


@typecaster
def SchemaCast(value, schema):
    # Make sure value and schema are dicts
    _assert_isinstance(value, dict)
    _assert_isinstance(schema, dict)

    # Create output dictionary
    output = dict()

    # Loop over each key and value
    for _key, _value_type in schema.items():
        # Fetch the value from the dict
        _value = value.get(_key)

        # If the value type is a sub-schema
        if isinstance(_value_type, dict):
            # Update value type with sub-schema
            _value_type = SchemaCast[_value_type]

        # Cast the value and place in output
        output[_key] = _value_type(_value)

    # Make sure all items are valid
    return output


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
