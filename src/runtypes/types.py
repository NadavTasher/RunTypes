import os

from runtypes.typechecker import typechecker

def assert_isinstance(_value, _type):
    # Check the value and type accordingly
    if not isinstance(_value, _type):
        raise TypeError("Value is not an instance of %r" % _type)


@typechecker
def Any(value):
    return value


@typechecker
def Optional(value, optional_type=Any):
    # Return if value is none
    if value is None:
        return

    # Check the optional type
    if not isinstance(value, optional_type):
        raise TypeError("Value is not an instance of %r" % optional_type)

    # Validate further
    return optional_type(value)


@typechecker
def Union(value, *value_types):
    # Validate value with types
    for value_type in value_types:
        if isinstance(value, value_type):
            return value_type(value)

    # Raise a value error
    raise TypeError("Value is not an instance of one of the following types: %r" % value_types)


@typechecker
def Literal(value, *literal_values):
    # Make sure value exists
    if value not in literal_values:
        raise TypeError("Value is not one of %r" % literal_values)

    # Return the value
    return value


@typechecker
def Text(value):
    # Make sure the value is an instance of a string
    # In Python 2, u"".__class__ returns unicode
    # In Python 3, u"".__class__ returns str
    assert_isinstance(value, (str, u"".__class__))

    # Return the value
    return value


@typechecker
def Bytes(value):
    # Make sure the value is an instance of bytes
    assert_isinstance(value, bytes)

    # Return the value
    return value


@typechecker
def List(value, item_type=Any):
    # Make sure value is a list
    assert_isinstance(value, list)

    # Loop over value and check items
    for item in value:
        assert_isinstance(item, item_type)

    # Convert the list
    return list([item_type(item) for item in value])


@typechecker
def Dict(value, key_type=Any, value_type=Any):
    # Make sure value is a dictionary
    assert_isinstance(value, dict)

    # Loop over value and check items
    for _key, _value in value.items():
        # Check the key and value types
        assert_isinstance(_key, key_type)
        assert_isinstance(_value, value_type)

    # Loop over keys and values and check types
    return dict({key_type(key): value_type(value) for key, value in value.items()})


@typechecker
def Tuple(value, *item_types):
    # Make sure value is a tuple
    if not isinstance(value, tuple):
        raise TypeError("Value is not a tuple")

    # If types do not exist, return
    if not item_types:
        return value

    # Make sure value is of length
    if len(value) != len(item_types):
        raise TypeError("Value length is invalid")

    # Check all item types
    for item, item_type in zip(value, item_types):
        # Check the item type
        if not isinstance(item, item_type):
            raise TypeError("Item %r is not an instance of %r" % (item, item_types))

    # Loop over values in tuple and validate them
    return tuple(item_type(item) for item, item_type in zip(value, item_types))


@typechecker
def Integer(value):
    # Make sure value is an int
    if type(value) != int:
        raise TypeError("Value is not an integer")

    # Return the value
    return value


@typechecker
def Float(value):
    # Make sure value is an float
    if type(value) != float:
        raise TypeError("Value is not a float")

    # Return the value
    return value


@typechecker
def Bool(value):
    # Make sure the value is a bool
    if type(value) != bool:
        raise TypeError("Value is not a bool")

    # Return the value
    return value


@typechecker
def Schema(value, schema):
    # Make sure value is a dict
    if not isinstance(value, dict):
        raise TypeError("Value is not a dict")

    # Make sure schema is a dict
    if not isinstance(schema, dict):
        raise TypeError("Schema is not a dict")

    # Make sure all of the keys exist
    if set(value.keys()) - set(schema.keys()):
        raise TypeError("Value keys and schema keys are not equal")

    # Make sure all items are valid
    return {key: (value_type if not isinstance(value_type, dict) else Schema[value_type])(value.get(key)) for key, value_type in schema.items()}


@typechecker
def Charset(value, chars):
    # Make sure value is a string
    if not isinstance(value, Text):
        raise TypeError("Value is not an instance of %r" % Text)

    # Validate charset
    if any(char not in chars for char in value):
        raise TypeError("Value contains invalid characters")

    # Validation has passed
    return value


@typechecker
def Domain(value):
    # Make sure value is a string
    if not isinstance(value, Text):
        raise TypeError("Value is not an instance of %r" % Text)

    # Split to parts by dot
    parts = value.split(".")

    # Make sure all parts are not empty
    if not all(parts):
        raise TypeError("Domain parts are invalid")

    # Loop over parts and validate characters
    for part in parts:
        if not isinstance(part.lower(), Charset["abcdefghijklmnopqrstuvwxyz0123456789-"]):
            raise TypeError("Domain part contains invalid characters")

    # Validation has passed
    return value


@typechecker
def Email(value):
    # Make sure value is a string
    if not isinstance(value, Text):
        raise TypeError("Value is not an instance of %r" % Text)

    # Split into two (exactly)
    parts = value.split("@")

    # Make sure the length is 2
    if len(parts) != 2:
        raise TypeError("Email can't be split into address and domain")

    # Make sure all parts are not empty
    if not all(parts):
        raise TypeError("Email parts are empty")

    # Extract address and domain
    address, domain = parts

    # Make sure the domain is an FQDN
    if not isinstance(domain, Domain):
        raise TypeError("Email domain is not an instance of %r" % Domain)

    # Make sure the address is valid
    for part in address.split("."):
        # Make sure part is not empty
        if not part:
            raise TypeError("Email address part is empty")

        # Make sure part matches charset
        if not isinstance(part, Charset["abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'*+-/=?^_`{|}~"]):
            raise TypeError("Email address part contains invalid characters")

    # Validation has passed
    return value


@typechecker
def Path(value):
    # Make sure value is a string
    if not isinstance(value, Text):
        raise TypeError("Value is not an instance of %r" % Text)

    # Convert the path into a normal path
    value = os.path.normpath(value)

    # Split the path by separator
    for part in value.split(os.path.sep):
        # Make sure the part is a valid path name
        if not isinstance(part, PathName):
            raise TypeError("Value part is not an instance of %r" % Text)

    # Path is valid
    return value


@typechecker
def PathName(value):
    # Make sure value is a string
    if not isinstance(value, Text):
        raise TypeError("Value is not an instance of %r" % Text)

    # Convert the path into a normal path
    value = os.path.normpath(value)

    # Make sure there are not path separators in the value
    if os.path.sep in value:
        raise TypeError("Path name contains path separator")

    # Make sure the path does not contain invalid characters
    for char in value:
        # Check for forbidden characters
        if char in ':"*?<>|':
            raise TypeError("Path name contains invalid characters")

    # Pathname is valid
    return value


# Initialize some charsets
ID = Charset["abcdefghijklmnopqrstuvwxyz0123456789"]
Binary = Charset["01"]
Decimal = Charset["0123456789"]
Hexadecimal = Charset["0123456789ABCDEFabcdef"]
