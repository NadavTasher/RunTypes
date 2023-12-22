import os

from runtypess.typechecker import typechecker


@typechecker
def Any(value):
    return value


@typechecker
def Union(value, *value_types):
    # Validate value with types
    for value_type in value_types:
        if isinstance(value, value_type):
            return value

    # Raise a value error
    raise TypeError("Value is not one of the following types - %r" % value_types)


@typechecker
def Intersection(value, *value_types):
    # Validate value with types
    for value_type in value_types:
        value = value_type(value)

    # Validation has passed
    return value


@typechecker
def Literal(value, *literal_values):
    # Make sure value exists
    if value not in literal_values:
        raise TypeError("Value is not one of %r" % literal_values)

    # Return the value
    return value


@typechecker
def Optional(value, optional_type=Any):
    # Return if value is none
    if value is None:
        return value

    # Validate further
    return optional_type(value)


@typechecker
def Text(value):
    # Make sure the value is an instance of a string
    # In Python 2, u"".__class__ returns unicode
    # In Python 3, u"".__class__ returns str
    if not isinstance(value, (str, u"".__class__)):
        raise TypeError("Value is not text")

    # Return the value
    return value


@typechecker
def Bytes(value):
    # Make sure the value is an instance of bytes
    if not isinstance(value, bytes):
        raise TypeError("Value is not bytes")

    # Return the value
    return value


@typechecker
def List(value, item_type=Any):
    # Make sure value is a list
    if not isinstance(value, list):
        raise TypeError("Value is not a list")

    # Loop over value and check items
    return list(item_type(item) for item in value)


@typechecker
def Dict(value, key_type=Any, value_type=Any):
    # Make sure value is a dictionary
    if not isinstance(value, dict):
        raise TypeError("Value is not a dict")

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
        raise TypeError("Value and schema keys are not equal")

    # Make sure all items are valid
    return {key: (value_type if not isinstance(value_type, dict) else Schema[value_type])(value.get(key)) for key, value_type in schema.items()}


@typechecker
def Charset(value, chars):
    # Make sure value is a string
    value = Text(value)

    # Validate charset
    if any(char not in chars for char in value):
        raise TypeError("Value contains invalid characters")

    # Validation has passed
    return value


@typechecker
def Domain(value):
    # Make sure value is a string
    value = Text(value)

    # Split to parts by dot
    parts = value.split(".")

    # Make sure all parts are not empty
    if not all(parts):
        raise TypeError("Value parts are invalid")

    # Loop over parts and validate characters
    for part in parts:
        part = Charset["abcdefghijklmnopqrstuvwxyz0123456789-"](part.lower())

    # Validation has passed
    return value


@typechecker
def Email(value):
    # Make sure value is a string
    value = Text(value)

    # Split into two (exactly)
    parts = value.split("@")

    # Make sure the length is 2
    if len(parts) != 2:
        raise TypeError("Value can't be split correctly")

    # Make sure all parts are not empty
    if not all(parts):
        raise TypeError("Value parts are invalid")

    # Extract address and domain
    address, domain = parts

    # Make sure the domain is an FQDN
    domain = Domain(domain)

    # Make sure the address is valid
    for part in address.split("."):
        # Make sure part is not empty
        if not part:
            raise TypeError("Value address part is invalid")

        # Make sure part matches charset
        part = Charset["abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'*+-/=?^_`{|}~"](part)

    # Validation has passed
    return value


@typechecker
def Path(value):
    # Make sure the value is text or bytes
    value = Union[Text, Bytes](value)

    # Convert the path into a normal path
    value = os.path.normpath(value)

    # Split the path by separator
    for part in value.split(os.path.sep):
        # Make sure the part matches the charset
        path = PathName(part)

    # Path is valid
    return path


@typechecker
def PathName(value):
    # Make sure the value is text or bytes
    value = Union[Text, Bytes](value)

    # Convert the path into a normal path
    value = os.path.normpath(value)

    # Make sure there are not path separators in the value
    if os.path.sep in value:
        raise TypeError("Value must not contain path separator")

    # Make sure the path does not contain invalid characters
    for char in value:
        # Check for forbidden characters
        if char in ':"*?<>|':
            raise TypeError("Value must not contain invalid characters")

    # Pathname is valid
    return value


# Initialize some charsets
ID = Charset["abcdefghijklmnopqrstuvwxyz0123456789"]
Binary = Charset["01"]
Decimal = Charset["0123456789"]
Hexadecimal = Charset["0123456789ABCDEFabcdef"]
