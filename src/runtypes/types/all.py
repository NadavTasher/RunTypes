import os
import re
import collections.abc

from runtypes.types.checker import TypeChecker
from runtypes.utilities.asserts import _assert, _assert_istype, _assert_isinstance

# Any typechecker is a lambda short-circut
Any = TypeChecker(lambda value: value, name="Any")


def _optional(value, optional_type=Any):
    # Return if value is none
    if value is None:
        return

    # Check the optional type
    _assert_isinstance(value, optional_type)

    # Validate further
    return value

Optional = TypeChecker(_optional, name="Optional")



def _union(value, *value_types):
    # Validate value with types
    for value_type in value_types:
        if isinstance(value, value_type):
            return value

    # Raise a value error
    raise TypeError(f"Value is not an instance of one of the following types: {value_types!r}")


Union = TypeChecker(_union, name="Union")

def _literal(value, *literal_values):
    # Make sure value exists
    _assert(value in literal_values, f"Value is not one of {literal_values}")

    # Return the value
    return value

Literal = TypeChecker(_literal, name="Literal")


def _str(value):
    # Make sure the value is an instance of a string
    _assert_isinstance(value, str)

Text = TypeChecker(str, _str, name="Text")
AnyStr = TypeChecker(str, _str, name="AnyStr")


def _bytes(value):
    # Make sure the value is an instance of bytes
    _assert_isinstance(value, bytes)

ByteString = TypeChecker(bytes, _bytes, name="ByteString")


def _list_check(value, item_type=Any):
    # Make sure value is a list
    _assert_isinstance(value, list)

    # Loop over value and check items
    for item in value:
        _assert_isinstance(item, item_type)

def _list_cast(value, item_type=Any):
    # Make sure value is a list
    _assert_isinstance(value, collections.abc.Sequence)

    # Loop over value and cast items
    return [item_type(item) for item in value]

List = TypeChecker(_list_cast, _list_check, name="List")




def _dict_cast(value, key_type, value_type):
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

Dict = TypeChecker(_dict_cast, _dict_check, name="Dict")

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

Tuple = TypeChecker(_tuple_cast, _tuple_check, name="Tuple")

def _schema_cast(value, schema):
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

def _schema_check(value, schema):
    # Make sure value and schema are dicts
    _assert_isinstance(value, dict)
    _assert_isinstance(schema, dict)

    # Loop over each key and value
    for _key, _value_type in schema.items():
        # Fetch the value from the dict
        _value = value.get(_key)

        # If the value type is a sub-schema
        if isinstance(_value_type, dict):
            # Update value type with sub-schema
            _value_type = Schema[_value_type]

        # Validate the value
        _assert_isinstance(_value, _value_type)

    # Make sure all items are valid
    return value

Schema = TypeChecker(_schema_cast, _schema_check, name="Schema")

@typechecker
def Domain(value):
    # Make sure value is a string
    _assert_isinstance(value, Text)

    # Split to parts by dot
    parts = value.split(".")

    # Make sure all parts are not empty
    _assert(all(parts), "Value parts are invalid")

    # Loop over parts and validate characters
    for part in parts:
        _assert_isinstance(part.lower(), Charset["abcdefghijklmnopqrstuvwxyz0123456789-"])

    # Validation has passed
    return value


@typechecker
def Email(value):
    # Make sure value is a string
    _assert_isinstance(value, Text)

    # Split into two (exactly)
    parts = value.split("@")

    # Make sure the length is 2
    _assert(len(parts) == 2, "Value can't be split into address and domain")

    # Make sure all parts are not empty
    _assert(all(parts), "Value address and domain are empty")

    # Extract address and domain
    address, domain = parts

    # Make sure the domain is an FQDN
    _assert_isinstance(domain, Domain)

    # Make sure the address is valid
    for part in address.split("."):
        # Make sure part is not empty
        _assert(part, "Value part is empty")

        # Make sure part matches charset
        _assert_isinstance(part.lower(), Charset["abcdefghijklmnopqrstuvwxyz0123456789+-_"])

    # Validation has passed
    return value


@typechecker
def Path(value):
    # Make sure value is a string
    _assert_isinstance(value, Text)

    # Create normal path from value
    normpath = os.path.normpath(value)

    # Make sure the path is safe to use
    _assert(value in [normpath, normpath + os.path.sep], "Value is invalid")

    # Split the path by separator
    for part in normpath.split(os.path.sep):
        # Make sure the part is a valid path name
        _assert_isinstance(part, PathName)

    # Path is valid
    return value


@typechecker
def PathName(value):
    # Make sure value is a string
    _assert_isinstance(value, Text)

    # Convert the path into a normal path
    value = os.path.normpath(value)

    # Make sure there are not path separators in the value
    _assert(os.path.sep not in value, "Value contains path separator")

    # Make sure the path does not contain invalid characters
    for char in value:
        # Check for forbidden characters
        _assert(char not in ':"*?<>|', "Value contains invalid characters")

    # Pathname is valid
    return value


@typechecker
def Pattern(value, pattern, flags=re.DOTALL):
    # Compile the pattern
    match = re.match(pattern, value, flags)

    # Make sure a match was found
    _assert(match is not None, "Value did not match pattern")

    # Make sure the match is a full match
    _assert(match.string == value, "Value did not match pattern")

    # Pattern was matched
    return value


@typechecker
def Charset(value, chars):
    # Make sure value is a string
    _assert_isinstance(value, Text)

    # Validate charset
    for char in value:
        _assert(char in chars, "Value contains invalid characters")

    # Validation has passed
    return value


# Initialize some charsets
ID = Charset["abcdefghijklmnopqrstuvwxyz0123456789"]
Binary = Charset["01"]
Decimal = Charset["0123456789"]
Hexadecimal = Charset["0123456789ABCDEFabcdef"]
