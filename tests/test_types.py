import pytest

from runtype.types import *


def test_any():
    assert Any(10) == 10
    assert isinstance(None, Any)
    assert isinstance("Hello World", Any)


def test_union():
    assert Union[Text, Integer](10) == 10
    assert isinstance("Hello World", Union[Text, Integer])
    assert isinstance(42, Union[Text, Integer])
    assert not isinstance(42.0, Union[Text, Integer])


def test_intersection():
    assert Intersection[Text, Email]("hello@local.host") == "hello@local.host"
    assert isinstance("hello@localhost", Intersection[Text, Email])
    assert not isinstance("hello", Intersection[Text, Email])


def test_literal():
    assert Literal[1, 2](1) == 1
    assert isinstance("Hello World", Literal["Hello World", 42])
    assert isinstance(42, Literal["Hello World", 42])
    assert not isinstance("Test", Literal["Hello World", 42])


def test_optional():
    assert Optional("A") == "A"
    assert Optional[Text]("A") == "A"
    assert isinstance(None, Optional[Text])
    assert isinstance("Hello World", Optional[Text])
    assert not isinstance(0, Optional[Text])


def test_text():
    assert Text("Hello") == "Hello"
    assert isinstance("Hello World", Text)
    assert isinstance(u"Hello World", Text)
    assert not isinstance(0, Text)


def test_bytes():
    assert Bytes(b"Hello") == b"Hello"
    assert isinstance(b"Hello World", Bytes)
    assert not isinstance(0, Bytes)


def test_list():
    assert List[Union[Text, Integer]](["1", 2]) == ["1", 2]
    assert isinstance(["Hello", "World", 42], List)
    assert not isinstance(["Hello", "World", 42], List[Text])


def test_dict():
    assert Dict[Text, Integer]({"a": 1}) == {"a": 1}
    assert isinstance({"hello": "world", "test": "test"}, Dict[Text, Text])
    assert not isinstance({"hello": "world", "test": 42}, Dict[Text, Text])


def test_tuple():
    assert Tuple((1, 2)) == (1, 2)
    assert Tuple[Integer, Integer]((1, 2)) == (1, 2)
    assert isinstance((1, 2, 3), Tuple[Integer, Integer, Integer])
    assert isinstance((1, 2, 3, "Hello World"), Tuple[Integer, Integer, Integer, Text])
    assert not isinstance((1, 2, 3, "Hello World"), Tuple[Integer, Integer, Integer, Integer])
    assert not isinstance("Hello World", Tuple[Integer, Integer, Integer])


def test_integer():
    assert Integer(1) == 1
    assert isinstance(1, Integer)
    assert isinstance(2, Integer)
    assert not isinstance("1", Integer)
    assert not isinstance(False, Integer)
    assert not isinstance("Hello World", Integer)


def test_float():
    assert Float(1.1) == 1.1
    assert isinstance(1.1, Float)
    assert isinstance(float(1), Float)
    assert not isinstance(1, Float)


def test_bool():
    assert Bool(True) == True
    assert isinstance(True, Bool)
    assert isinstance(False, Bool)
    assert not isinstance("True", Bool)
    assert not isinstance("False", Bool)
    assert not isinstance(0, Bool)
    assert not isinstance(1, Bool)


def test_schema():
    schema = Schema[{"hello": Text, "number": Integer, "boolean": Bool, "list-of-names": List[Text], "mapping-of-numbers": Dict[Union[Integer, Float], Text]}]
    assert schema({"hello": "World", "number": 42, "boolean": True, "list-of-names": ["Jack", "James", "John"], "mapping-of-numbers": {42: "Meaning of life", 3.14: "Value of Pi"}}) == {"hello": "World", "number": 42, "boolean": True, "list-of-names": ["Jack", "James", "John"], "mapping-of-numbers": {42: "Meaning of life", 3.14: "Value of Pi"}}
    assert isinstance({"hello": "World", "number": 42, "boolean": True, "list-of-names": ["Jack", "James", "John"], "mapping-of-numbers": {42: "Meaning of life", 3.14: "Value of Pi"}}, schema)
    assert not isinstance({"hello": "World", "number": 42, "boolean": True, "list-of-names": ["Jack", "James", "John"], "mapping-of-numbers": {42: "Meaning of life", 3.14: "Value of Pi", "Test": "Hello World"}}, schema)


def test_charset():
    assert Charset["HeloWrd "]("Hello World") == "Hello World"
    assert isinstance("Hello World", Charset["HeloWrd "])
    assert not isinstance("Test", Charset["HeloWrd "])


def test_domain():
    assert Domain("localhost") == "localhost"
    assert isinstance("localhost", Domain)
    assert isinstance("local.host", Domain)
    assert not isinstance("", Domain)
    assert not isinstance(".", Domain)
    assert not isinstance(".host", Domain)
    assert not isinstance("local.", Domain)


def test_email():
    assert Email("hello.world@localhost") == "hello.world@localhost"
    assert isinstance("hello.world@localhost", Email)
    assert isinstance("hello@local.host", Email)
    assert not isinstance(".hello@localhost", Email)
    assert not isinstance("@local.host", Email)
    assert not isinstance(".@local.host", Email)
    assert not isinstance("hello.world@", Email)
    assert not isinstance("hello.world@.", Email)


def test_id():
    assert ID("asdasdasd") == "asdasdasd"
    assert isinstance("asdasdasd", ID)
    assert not isinstance("asdasdasd=", ID)


def test_binary():
    assert Binary("00101101") == "00101101"
    assert isinstance("00101101", Binary)
    assert not isinstance("00101102", Binary)


def test_decimal():
    assert Decimal("1234") == "1234"
    assert isinstance("1234", Decimal)
    assert not isinstance("0x1234", Decimal)


def test_hexadecimal():
    assert Hexadecimal("badc0ffe") == "badc0ffe"
    assert isinstance("badc0ffe", Hexadecimal)
    assert not isinstance("badcoffe", Hexadecimal)
