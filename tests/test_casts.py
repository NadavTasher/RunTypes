import pytest

from runtypes.casts import *
from runtypes.types import Text, Integer, Bool, List


def test_list_cast():
    assert ListCast[int](["1", 2]) == [1, 2]
    assert not isinstance(["Hello", "World", 42], ListCast[str])
    assert not isinstance(["Hello", 10], ListCast[Text])


def test_dict_cast():
    assert DictCast[str, int]({"a": "1"}) == {"a": 1}
    assert isinstance({"hello": "world", "test": "test"}, DictCast[Text, Text])
    assert not isinstance({"hello": "world", "test": 42}, DictCast[Text, str])
    assert not isinstance({"hello": "world", "test": 42}, DictCast[Text, Text])


def test_tuple_cast():
    assert TupleCast[int, int]((1, "2")) == (1, 2)
    assert not isinstance((1, "2"), TupleCast[int, int])
    assert isinstance((1, 2, 3), TupleCast[Integer, Integer, Integer])


def test_schema_cast():
    schema = SchemaCast[{"hello": int, "sub": {"thing": int}}]
    assert schema({"hello": "1", "sub": {"thing": True}}) == {"hello": 1, "sub": {"thing": 1}}
    assert isinstance({"hello": 1, "sub": {"thing": 1}}, schema)
    assert not isinstance({"hello": "1", "sub": {"thing": True}}, schema)


def test_charset_cast():
    assert CharsetCast["HeloWrd "]("Hello World!") == "Hello World"
    assert isinstance("Hello World", CharsetCast["HeloWrd "])
    assert not isinstance("Test", CharsetCast["HeloWrd "])


def test_id_cast():
    assert IDCast("asdasdasd?") == "asdasdasd"
    assert isinstance("asdasdasd", IDCast)
    assert not isinstance("asdasdasd?", IDCast)


def test_binary_cast():
    assert BinaryCast("001011012") == "00101101"
    assert isinstance("00101101", BinaryCast)
    assert not isinstance("001011012", BinaryCast)


def test_decimal_cast():
    assert DecimalCast("1234F") == "1234"
    assert DecimalCast("0x1234F") == "01234"
    assert isinstance("1234", DecimalCast)
    assert not isinstance("0x1234", DecimalCast)


def test_hexadecimal_cast():
    assert HexadecimalCast("badc0ffeZ") == "badc0ffe"
    assert isinstance("badc0ffe", HexadecimalCast)
    assert not isinstance("badc0ffeZ", HexadecimalCast)
