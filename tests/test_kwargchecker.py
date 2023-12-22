import pytest

from runtypes.types import Literal, Intersection
from runtypes.kwargchecker import kwargchecker


def test_kwargchecker():

    @kwargchecker(integer=Intersection[Literal[10], int])
    def target(integer):
        print("Got %d" % integer)

    # Test with good argument
    with pytest.raises(TypeError):
        # This should not work
        target(integer=42)

    # This should work
    target(integer=10)
