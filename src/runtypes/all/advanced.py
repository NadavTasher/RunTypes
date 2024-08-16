import os
import re
import typing

from runtypes.runtype import RunType, _assert, _assert_istype, _assert_isinstance
from runtypes.all.basic import Any, AnyStr


def _schema_cast(value, schema) -> dict:
    # Make sure value and schema are dicts
    _assert_isinstance(value, dict)
    _assert_isinstance(schema, dict)

    # Create output dictionary
    output = {}

    # Loop over each key and value
    for _key, _value_type in schema.items():
        # Fetch the value from the dict
        _value = value.get(_key)

        # If the value type is a sub-schema
        if isinstance(_value_type, dict):
            # Cast value recusrively
            output[_key] = _schema_cast(_value, _value_type)
        else:
            # Cast the value and place in output
            output[_key] = _value_type(_value)

    # Make sure all items are valid
    return output


def _schema_check(value, schema) -> None:
    # Make sure value and schema are dicts
    _assert_isinstance(value, dict)
    _assert_isinstance(schema, dict)

    # Loop over each key and value
    for _key, _value_type in schema.items():
        # Fetch the value from the dict
        _value = value.get(_key)

        # If the value type is a sub-schema
        if isinstance(_value_type, dict):
            # Check value recursively
            _schema_check(_value, _value_type)
        else:
            # Validate the value
            _assert_isinstance(_value, _value_type)

def _charset_cast(value, chars):
    # Make sure value is a string
    _assert_isinstance(value, AnyStr)

    # Return the string with only the valid characters
    return str().join(char for char in value if char in chars)

def _charset_check(value, chars):
    # Make sure value is a string
    _assert_isinstance(value, AnyStr)

    # Validate charset
    for char in value:
        _assert(char in chars, "Value contains invalid characters")


def _domain_check(value) -> None:
    # Make sure value is a string
    _assert_isinstance(value, AnyStr)

    # Split to parts by dot
    parts = value.split(".")

    # Make sure all parts are not empty
    _assert(all(parts), "Value parts are invalid")

    # Loop over parts and validate characters
    for part in parts:
        _assert_isinstance(part.lower(), Charset["abcdefghijklmnopqrstuvwxyz0123456789-"])


def _email_check(value: typing.Any) -> None:
    # Make sure value is a string
    _assert_isinstance(value, AnyStr)

    # Split into two (exactly)
    parts = value.split("@")

    # Make sure the length is 2
    _assert(len(parts) == 2, "Value can't be split into address and domain")

    # Make sure all parts are not empty
    _assert(all(parts), "Value address and domain are empty")

    # Extract address and domain
    address, domain = parts

    # Make sure the domain is an FQDN
    _domain_check(domain)

    # Make sure the address is valid
    for part in address.split("."):
        # Make sure part is not empty
        _assert(part, "Value part is empty")

        # Make sure part matches charset
        _assert_isinstance(part.lower(), Charset["abcdefghijklmnopqrstuvwxyz0123456789+-_"])

    # Validation has passed
    return value

def _pathname_check(value):
    # Make sure value is a string
    _assert_isinstance(value, AnyStr)

    # Convert the path into a normal path
    value = os.path.normpath(value)

    # Make sure there are not path separators in the value
    _assert(os.path.sep not in value, "Value contains path separator")

    # Make sure the path does not contain invalid characters
    for char in value:
        # Check for forbidden characters
        _assert(char not in ':"*?<>|', "Value contains invalid characters")

def _path_check(value):
    # Make sure value is a string
    _assert_isinstance(value, AnyStr)

    # Create normal path from value
    normpath = os.path.normpath(value)

    # Make sure the path is safe to use
    _assert(value in [normpath, normpath + os.path.sep], "Value is invalid")

    # Split the path by separator
    for part in normpath.split(os.path.sep):
        # Make sure the part is a valid path name
        _pathname_check(part)


def _pattern_check(value, pattern, flags=re.DOTALL):
    # Compile the pattern
    match = re.match(pattern, value, flags)

    # Make sure a match was found
    _assert(match is not None, "Value did not match pattern")

    # Make sure the match is a full match
    _assert(match.string == value, "Value did not match pattern")


# Generic types
Schema = RunType("Schema", caster=_schema_cast, checker=_schema_check)
Charset = RunType("Charset", caster=_charset_cast, checker=_charset_check)

# Path types
Path = RunType("Path", checker=_path_check)
PathName = RunType("PathName", checker=_pathname_check)

# Advanced types
Email = RunType("Email", checker=_email_check)
Domain = RunType("Domain", checker=_domain_check)
Pattern = RunType("Pattern", checker=_pattern_check)

# Additional charsets
ID = Charset["abcdefghijklmnopqrstuvwxyz0123456789"]
Binary = Charset["01"]
Decimal = Charset["0123456789"]
Hexadecimal = Charset["0123456789ABCDEFabcdef"]