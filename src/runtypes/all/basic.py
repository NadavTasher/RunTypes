import os
import re
import collections.abc

from runtypes.runtype import RunType, _assert, _assert_istype, _assert_isinstance

# Any is the most basic type and is used by other types, hence defined here
Any = RunType("Any", lambda value: value)


def _optional(value, optional_type=Any):
    # Return if value is none
    if value is None:
        return

    # Check the optional type
    _assert_isinstance(value, optional_type)

    # Validate further
    return value


def _union(value, *value_types):
    # Validate value with types
    for value_type in value_types:
        if isinstance(value, value_type):
            return value

    # Raise a value error
    raise TypeError(f"Value is not an instance of one of the following types: {value_types!r}")


def _literal(value, *literal_values):
    # Make sure value exists
    _assert(value in literal_values, f"Value is not one of {literal_values}")

    # Return the value
    return value


def _string_check(value):
    # Make sure the value is an instance of a string
    _assert_isinstance(value, (str, u"".__class__))


def _bytestring_check(value):
    # Make sure the value is an instance of bytes
    _assert_isinstance(value, (bytes, bytearray))


def _list_cast(value, item_type=Any):
    # Make sure value is a list
    _assert_isinstance(value, collections.abc.Sequence)

    # Loop over value and cast items
    return [item_type(item) for item in value]


def _list_check(value, item_type=Any):
    # Make sure value is a list
    _assert_isinstance(value, list)

    # Loop over value and check items
    for item in value:
        _assert_isinstance(item, item_type)


def _dict_cast(value, key_type=Any, value_type=Any):
    # Make sure value is a dictionary
    _assert_isinstance(value, collections.abc.Mapping)

    # Loop over value and cast items
    return {key_type(_key): value_type(_value) for _key, _value in value.items()}


def _dict_check(value, key_type=Any, value_type=Any):
    # Make sure value is a dictionary
    _assert_isinstance(value, dict)

    # Loop over value and check items
    for _key, _value in value.items():
        # Check the key and value types
        _assert_isinstance(_key, key_type)
        _assert_isinstance(_value, value_type)

    # Loop over keys and values and check types
    return value


def _tuple_cast(value, *item_types):
    # Make sure value is a tuple
    _assert_isinstance(value, collections.abc.Sequence)

    # Make sure value is of length
    _assert(len(value) == len(item_types), "Value length does not match types")

    # Check all item types
    return tuple(item_type(item) for item, item_type in zip(value, item_types))


def _tuple_check(value, *item_types):
    # Make sure value is a tuple
    _assert_isinstance(value, tuple)

    # If types do not exist, return
    if not item_types:
        return value

    # Make sure value is of length
    _assert(len(value) == len(item_types), "Value length does not match types")

    # Check all item types
    for item, item_type in zip(value, item_types):
        # Check the item type
        _assert_isinstance(item, item_type)

    # Loop over values in tuple and validate them
    return value


# Generic types
Union = RunType("Union", _union)
Literal = RunType("Literal", _literal)
Optional = RunType("Optional", _optional)

# Text and byte types
Text = RunType("Text", str, _string_check)
AnyStr = RunType("AnyStr", str, _string_check)
ByteString = RunType("ByteString", bytes, _bytestring_check)

# Container types
List = RunType("List", _list_cast, _list_check)
Dict = RunType("Dict", _dict_cast, _dict_check)
Tuple = RunType("Tuple", _tuple_cast, _tuple_check)
